from llama import Llama, Dialog

from custom_types import DLlamaGResponse
from exceptions import ChatCompleteException

from typing import List, Optional

class ChatBot:
    """
    Wrapper for Meta's LLaMA large language model

    @param str ckpt_dir: Path to model checkpoints
    @param str tokenizer_path: Path to model tokenizer
    @param float top_p: Top-p probability threshold for nucelus sampling
    @param int max_batch_size: Maximum batch size for inference
    @param int max_seq_len: Maximum sequence length for input text
    @param Optional[int] max_gen_len: Maximum length of generated text sequence
    @param float temperature: Temperature value for controlling randomness in sampling
    @param bool build: Whether to build the LLaMA model or use the dummy
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
        """
        Generates a chat response using LLaMA model based off input sequences

        @param List[Dialog] dialogs: Input dialog sequences

        @returns DLlamaGResponse: Response from model
        """
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
        """
        Generates a response using the last entry in the input sequence

        @param List[Dialog] dialogs: Input dialog sequences

        @returns DLlamaGResponse: Dummy response
        """
        try:
            lastMessage: str = dialogs[-1]["content"]
            return DLlamaGResponse(
                last_message=lastMessage,
                response=f"You just said: '{lastMessage}'"
            )
        except Exception as e:
            raise ChatCompleteException(f"Could not complete chat due to: {e}")