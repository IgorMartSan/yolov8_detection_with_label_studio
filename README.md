poetry source add -p explicit pytorch pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

## Adicionando pytorch no poetry 

Como executar a seguinte comando para usar o cuda no ambiente Poetry ? (poetry source add -p explicit pytorch https://download.pytorch.org/whl/cu118
poetry add --source pytorch torch torchvision)

Siga o tutorial:
Adicionar no poetry
poetry source add -p explicit pytorch https://download.pytorch.org/whl/cu118

Instalar usando
poetry add --source pytorch torch torchvision


## Não use o poetry 

Instalar na sequência:

1 - pytorch

2 - ultralitics

Na ultima vez precisei deletar o pytorch e o ultralitics.
