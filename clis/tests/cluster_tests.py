from core.cli.application import ContextApplication
from core.cli.async_module import CoroCLI
from core.cli.main import console_command
from core.cli.models import OptionCMD
from core.cli.processor import GenericCLI
from modules.cluster.ascender_ai import AscenderAIChat

class ClusterTestsCLI(GenericCLI):
    app_name: str = "test-clis"
    description: str = "CLI for testing cluster"

    def __init__(self) -> None:
        self.ai_cluster_chat = AscenderAIChat("mixtral-8x7b", verbose=True, max_tokens=100)

    @console_command()
    @CoroCLI()
    async def completions(self, ctx: ContextApplication, streaming: bool = OptionCMD("streaming", ctype=bool)):
        message = input("Enter message: ")
        
        self.ai_cluster_chat.streaming = streaming
        completion = await self.ai_cluster_chat.get_completion(message)

        if streaming:
            ctx.console_print(f"[yellow]AI", end=" ")
            async for choice in completion:
                ctx.console_print(f"{choice['choices'][0]['text']}", flush=None, end="")
            
            return
        
        ctx.console_print(f"[yellow]AI: {completion['choices'][0]['text']}[/yellow][cyan]")