from tkinter import ttk, messagebox
from datetime import datetime
from plyer import notification
import tkinter as tk
import webbrowser
import json
import sys
import os

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class AnimeReminder:
    def __init__(self, root):
        self.root = root
        self.root.title("Lembrete de Animes")
        self.root.iconbitmap(resource_path("icone.ico"))
        self.root.geometry("850x600")
        self.filename = "animes.json"

        # --- Carrega o tema Azure ---
        style = ttk.Style(self.root)
        try:
            theme_path = os.path.join(os.path.dirname(__file__), "theme", "azure-dark.tcl")
            self.root.tk.call("source", theme_path)
            style.theme_use("azure-dark")
        except tk.TclError:
            messagebox.showerror("Erro de Tema", "Não foi possível encontrar o arquivo 'theme/azure-dark.tcl'.")
            self.root.destroy()
            return

        # --- Força a aplicação do tema em todos os cantos ---
        BG_COLOR = "#333333"
        FG_COLOR = "#ffffff"
        FIELD_BG_COLOR = "#3E3E3E" # Cor de fundo para campos

        self.root.configure(background=BG_COLOR)
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR)
        style.configure("TButton", foreground=FG_COLOR)

        # --- NOVAS LINHAS PARA CORRIGIR O TEXTO PRETO ---
        style.configure("TEntry", foreground=FG_COLOR, fieldbackground=FIELD_BG_COLOR)
        style.configure("Treeview", foreground=FG_COLOR, fieldbackground=FIELD_BG_COLOR)

        # Frame para os campos de entrada
        frame_entrada = ttk.Frame(self.root, padding="10")
        frame_entrada.pack(fill='x', padx=10, pady=5)
        frame_entrada.columnconfigure(1, weight=1)

        # Labels e Entradas
        ttk.Label(frame_entrada, text="Nome do Anime:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_nome = ttk.Entry(frame_entrada, width=50)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(frame_entrada, text="Data (DD/MM/AAAA):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_data = ttk.Entry(frame_entrada)
        self.entry_data.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(frame_entrada, text="Link para Assistir:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_link = ttk.Entry(frame_entrada)
        self.entry_link.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(frame_entrada, text="Episódios (Ex: 1/12):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_eps = ttk.Entry(frame_entrada)
        self.entry_eps.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        # Frame para os botões
        frame_botoes = ttk.Frame(self.root, padding="10")
        frame_botoes.pack(fill='x', padx=10)

        self.add_button = ttk.Button(frame_botoes, text="Adicionar Anime", command=self.adicionar_anime)
        self.add_button.pack(side='left', padx=5)

        self.edit_button = ttk.Button(frame_botoes, text="Editar Selecionado", command=self.open_edit_window)
        self.edit_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(frame_botoes, text="Deletar Selecionado", command=self.deletar_anime)
        self.delete_button.pack(side='left', padx=5)

        # Lista de Animes (Treeview)
        tree_frame = ttk.Frame(self.root, padding="10")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("Nome", "Data", "Episódios", "Link"), show="headings")
        self.tree.heading("Nome", text="Nome do Anime")
        self.tree.heading("Data", text="Próximo Lançamento")
        self.tree.heading("Episódios", text="Progresso")
        self.tree.heading("Link", text="Link")

        self.tree.column("Nome", width=300)
        self.tree.column("Data", width=120, anchor='center')
        self.tree.column("Episódios", width=100, anchor='center')
        self.tree.column("Link", width=300)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Eventos
        self.tree.bind("<Double-1>", self.abrir_link)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Carregar dados e iniciar verificador
        self.load_animes()
        self.check_for_notifications()

    # --- Métodos de Funcionalidade ---

    def adicionar_anime(self):
        nome = self.entry_nome.get()
        data = self.entry_data.get()
        link = self.entry_link.get()
        eps = self.entry_eps.get()

        if not (nome and data and link):
            messagebox.showwarning("Campos Vazios", "Por favor, preencha pelo menos os campos de Nome, Data e Link.", parent=self.root)
            return
        
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Data Inválida", "Por favor, insira a data no formato DD/MM/AAAA.", parent=self.root)
            return
        
        self.tree.insert("", "end", values=(nome, data, eps, link))
        self.entry_nome.delete(0, 'end')
        self.entry_data.delete(0, 'end')
        self.entry_link.delete(0, 'end')
        self.entry_eps.delete(0, 'end')
        self.save_animes()

    def deletar_anime(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Nenhuma Seleção", "Por favor, selecione um anime na lista para deletar.", parent=self.root)
            return
        
        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja deletar o anime selecionado?", parent=self.root):
            self.tree.delete(selected_item)
            self.save_animes()

    def abrir_link(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            values = self.tree.item(item_id, 'values')
            link = values[3]
            if link and (link.startswith("http://") or link.startswith("https://")):
                webbrowser.open_new_tab(link)
            else:
                messagebox.showinfo("Link Inválido", "O link fornecido não é válido.", parent=self.root)
    
    # --- NOVO: Lógica de Edição ---

    def open_edit_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Nenhuma Seleção", "Por favor, selecione um anime para editar.", parent=self.root)
            return
        
        # Pega o primeiro item da seleção
        item_id = selected_item[0]
        current_values = self.tree.item(item_id, 'values')

        # Cria a janela de edição
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Editar Anime")
        edit_win.iconbitmap(resource_path("icone.ico"))
        edit_win.geometry("400x250")
        edit_win.transient(self.root) # Mantém a janela de edição na frente da principal
        edit_win.grab_set() # Bloqueia a janela principal enquanto edita
        edit_win.configure(background="#333333")

        frame = ttk.Frame(edit_win, padding="10")
        frame.pack(fill="both", expand=True)

        # Campos de entrada pré-preenchidos
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        edit_nome = ttk.Entry(frame, width=40)
        edit_nome.grid(row=0, column=1, padx=5, pady=5)
        edit_nome.insert(0, current_values[0])

        ttk.Label(frame, text="Data:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        edit_data = ttk.Entry(frame)
        edit_data.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        edit_data.insert(0, current_values[1])

        ttk.Label(frame, text="Episódios:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        edit_eps = ttk.Entry(frame)
        edit_eps.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        edit_eps.insert(0, current_values[2])
        
        ttk.Label(frame, text="Link:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        edit_link = ttk.Entry(frame)
        edit_link.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        edit_link.insert(0, current_values[3])

        # Botão para salvar
        save_button = ttk.Button(frame, text="Salvar Alterações", 
                                 command=lambda: self.save_edit(edit_win, item_id, edit_nome, edit_data, edit_eps, edit_link))
        save_button.grid(row=4, column=1, pady=10, sticky="e")

    def save_edit(self, edit_win, item_id, entry_nome, entry_data, entry_eps, entry_link):
        new_nome = entry_nome.get()
        new_data = entry_data.get()
        new_eps = entry_eps.get()
        new_link = entry_link.get()

        if not (new_nome and new_data and new_link):
            messagebox.showwarning("Campos Vazios", "Nenhum campo principal pode ficar vazio.", parent=edit_win)
            return

        try:
            datetime.strptime(new_data, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Data Inválida", "Por favor, insira a data no formato DD/MM/AAAA.", parent=edit_win)
            return

        # Atualiza o item na Treeview
        self.tree.item(item_id, values=(new_nome, new_data, new_eps, new_link))
        
        # Salva no arquivo JSON
        self.save_animes()

        # Fecha a janela de edição
        edit_win.destroy()

    # --- Métodos de Persistência e Notificação ---

    def save_animes(self):
        animes_list = []
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            anime_dict = {
                "nome": values[0],
                "data": values[1],
                "eps": values[2],
                "link": values[3]
            }
            animes_list.append(anime_dict)
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(animes_list, f, indent=4, ensure_ascii=False)

    def load_animes(self):
        if not os.path.exists(self.filename):
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                animes_list = json.load(f)
                for anime in animes_list:
                    self.tree.insert("", "end", values=(anime.get("nome"), anime.get("data"), anime.get("eps"), anime.get("link")))
        except (json.JSONDecodeError, TypeError):
            messagebox.showerror("Erro ao Carregar", "Não foi possível ler o arquivo de animes. Pode estar corrompido.", parent=self.root)

    def check_for_notifications(self):
        today_str = datetime.now().strftime("%d/%m/%Y")
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            anime_nome, anime_data = values[0], values[1]

            if anime_data == today_str:
                try:
                    notification.notify(
                        title="Lembrete de Anime!",
                        message=f"Hoje tem episódio novo de '{anime_nome}'. Não se esqueça de assistir!",
                        app_name="Lembrete de Animes",
                        timeout=20
                    )
                except Exception as e:
                    print(f"Erro ao enviar a notificação: {e}")
        
        self.root.after(3600000, self.check_for_notifications)

    def on_closing(self):
        self.save_animes()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimeReminder(root)
    root.mainloop()