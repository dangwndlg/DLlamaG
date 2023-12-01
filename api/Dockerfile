FROM ubuntu:latest

RUN apt update
RUN apt install python3 python3-pip -y
RUN alias python="python3"
RUN alias pip="pip3"

RUN mkdir -p /mnt/api
WORKDIR /mnt/api

ARG LLAMA_CKPT_DIR="llama/llama-2-7b-chat"
ARG LLAMA_TOKENIZER_PATH="llama/tokenizer.model"

ENV BUILD_LLAMA="true"
ENV ENABLE_LOGGING="true"
ENV LLAMA_CKPT_DIR="/mnt/api/llama/llama-2-7b-chat"
ENV LLAMA_TOKENIZER_PATH="/mnt/api/llama/tokenizer.model"

# Copy code
COPY . .

COPY ${LLAMA_CKPT_DIR} "./llama/llama-2-7b-chat/"
COPY ${LLAMA_TOKENIZER_PATH} "./llama/tokenizer.model"

RUN pip install -r ./requirements.txt

# CMD [ "torchrun", "--nproc_per_node", "1", "src/main.py" ]