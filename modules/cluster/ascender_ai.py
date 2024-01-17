import json
from aiohttp import ClientSession
from typing import Optional
from rich import print as rprint
from rich.panel import Panel


class AscenderAIChat:
    base_url: str = "http://178.252.103.102:8000"
    def __init__(self, model: str = "mistral-7b-instruct", *, 
                 max_tokens: int = 30, streaming: bool = False,
                 verbose: bool = False) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.streaming = streaming
        self.verbose = verbose
    
    async def get_completion(self, prompt: str, *, temperature: float = 0.9, 
                             stop_seqs: Optional[list[str]] = None, seed: Optional[int] = None):
        """
        Gets the completion prompt from the AI
        """
        # Verbose displaying of the prompt
        if self.verbose:
            panel = Panel(f"[bold green]{prompt}[/bold green]", title="Get completion request")
            rprint(panel)
        
        if self.streaming:
            return self._get_streaming_completion(prompt, temperature=temperature, stop=stop_seqs, seed=seed)
        else:
            async with ClientSession(base_url=self.base_url) as client:
                async with client.post("/completions/completions", json={
                    "prompt": prompt,
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "temperature": temperature,
                    "stop_seqs": stop_seqs,
                    "seed": seed,
                }) as resp:
                    response = await resp.json()
                    if self.verbose:
                        response_panel = Panel(f"[bold yellow]{prompt}[/bold yellow]", title="AI Response")
                        rprint(response_panel)
                    return response
    
    async def _get_streaming_completion(self, prompt: str, *, temperature: float = 0.9, 
                                        stop: Optional[list[str]] = None, seed: Optional[int] = None):
        async with ClientSession(base_url=self.base_url) as client:
            async with client.post("/completions/completions/stream", json={
                "prompt": prompt,
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": temperature,
                "stop_seqs": stop,
                "seed": seed,
            }) as resp:
                async for line in resp.content.iter_any():
                    try:
                        readed_line = line.decode()

                        readed_line.split("} {")
                        yield json.loads(readed_line)
                    except:
                        pass