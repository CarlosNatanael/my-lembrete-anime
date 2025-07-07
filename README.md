# Lembrete de Animes

Um aplicativo de desktop simples, criado com Python e Tkinter, para ajudar você a nunca mais perder o lançamento de um novo episódio de anime.

## ✨ Funcionalidades

- **Adicionar, Editar e Deletar Animes:** Gerencie sua lista de animes de forma fácil e intuitiva.
- **Armazenamento de Dados:** Salve informações essenciais como nome, próxima data de lançamento, progresso de episódios (Ex: "2/12") e o link para assistir.
- **Notificações de Lançamento:** Receba uma notificação na sua área de trabalho sempre que um anime da sua lista tiver um episódio programado para o dia atual.
- **Interface Dark Mode:** Um tema escuro moderno e agradável, baseado no tema Azure for Ttk, para uma melhor experiência visual.
- **Acesso Rápido:** Abra o link para assistir ao anime diretamente da lista com um duplo clique.
- **Persistência Local:** Todos os seus dados são salvos localmente em um arquivo `animes.json`.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Tkinter:** Para a construção da interface gráfica (GUI).
- **Plyer:** Para o sistema de notificações de desktop multiplataforma.
- **Azure ttk Theme:** Tema customizado para modernizar a aparência do Tkinter.
- **PyInstaller:** Para empacotar a aplicação em um executável (.exe).

## 🚀 Como Executar a Partir do Código-Fonte

Para rodar o projeto no seu ambiente de desenvolvimento, siga os passos abaixo:

1. **Pré-requisitos:**  
   Ter o Python 3 instalado.

2. **Clone este repositório:**
   ```bash
   git clone https://github.com/seu-usuario/my-lembrete-anime.git
   cd my-lembrete-anime
   ```

3. **Instale as dependências:**  
   A única dependência externa é a plyer.
   ```bash
   pip install plyer
   ```

4. **Execute o aplicativo:**
   ```bash
   python anime-rember.py
   ```