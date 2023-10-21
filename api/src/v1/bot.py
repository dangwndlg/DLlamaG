from llama import Llama, Dialog

from custom_types import DLlamaGResponse
from exceptions import ChatCompleteException

from typing import List, Optional

class ChatBot:
    """
    Wrapper for Meta's LLaMA large language model
    """
    def __init__(
        self,
        ckpt_dir: str,
        tokenizer_path: str,
        top_p: float = 0.9,
        max_batch_size: int = 10,
        max_seq_len: int = 256,
        max_gen_len: Optional[int] = None,
        temperature: float = 0.6,
        build: bool = True
    ) -> None:
        self.top_p = top_p
        self.max_seq_len = max_seq_len
        self.max_gen_len = max_gen_len
        self.temperature = temperature
        self.build = build

        if build:
            self.generator: Llama = Llama.build(
                ckpt_dir=ckpt_dir,
                tokenizer_path=tokenizer_path,
                max_seq_len=max_seq_len,
                max_batch_size=max_batch_size
            )

    async def chat_complete(self, dialogs: List[Dialog]) -> DLlamaGResponse:
        try:
            results = self.generator.chat_completion(
                dialogs=[dialogs],
                temperature=self.temperature,
                top_p=self.top_p,
                max_gen_len=self.max_gen_len
            )

            return DLlamaGResponse(
                last_message=dialogs[-1]["content"],
                response=results[0]["generation"]["content"]
            )
        except Exception as e:
            raise ChatCompleteException(f"Could not complete chat due to: {e}")

    async def dummy_chat_complete(self, dialogs: List[Dialog]) -> DLlamaGResponse:
        try:
            lastMessage: str = dialogs[-1]["content"]
            return DLlamaGResponse(
                last_message=lastMessage,
                response=f"You just said: '{lastMessage}'"
            )
        except Exception as e:
            raise ChatCompleteException(f"Could not complete chat due to: {e}")