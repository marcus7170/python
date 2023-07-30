import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from PIL import ImageTk, Image
import mysql.connector
from hashlib import sha256

# Função para criptografar a senha
def encrypt_password(password):
    return sha256(password.encode()).hexdigest()

# Função para registrar um novo usuário
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    # Verifica se os campos estão preenchidos
    if not username or not password:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Verifica se o usuário já existe
    cursor.execute("SELECT * FROM rpg_login WHERE user = %s", (username,))
    if cursor.fetchone() is not None:
        messagebox.showerror("Erro", "Usuário já existe.")
        return

    # Criptografa a senha antes de inserir no banco de dados
    encrypted_password = encrypt_password(password)

    # Insere o novo usuário no banco de dados
    cursor.execute("INSERT INTO rpg_login (user, senha) VALUES (%s, %s)", (username, encrypted_password))
    db_connection.commit()
    messagebox.showinfo("Sucesso", "Usuário registrado com sucesso.")
    show_character_selection()

# Função para fazer login
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    # Verifica se os campos estão preenchidos
    if not username or not password:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Verifica se o usuário existe e se a senha está correta
    cursor.execute("SELECT senha FROM rpg_login WHERE user = %s", (username,))
    result = cursor.fetchone()

    if result is None:
        messagebox.showerror("Erro", "Usuário não encontrado.")
    elif encrypt_password(password) == result[0]:
        messagebox.showinfo("Sucesso", "Login bem-sucedido.")
        show_game_window()
    else:
        messagebox.showerror("Erro", "Senha incorreta.")


def show_character_selection():
    window.withdraw()
    character_selection_window = tk.Toplevel()
    character_selection_window.title("Escolha de Personagem")

    # Labels
    character_label = tk.Label(character_selection_window, text="Escolha seu personagem:", font=("Arial", 14))
    character_label.pack()

    # Lista de personagens
    characters = tk.Listbox(character_selection_window, font=("Arial", 12), selectmode="single")
    characters.pack()

    # Adicionar os personagens à lista
    for personagem in personagens:
        characters.insert(tk.END, personagem["nome"])

    # Botão para confirmar a seleção
    confirm_button = ttk.Button(character_selection_window, text="Confirmar", command=lambda: confirm_character_selection(characters))
    confirm_button.pack()

def confirm_character_selection(characters):
    selected_character_index = characters.curselection()
    if selected_character_index:
        selected_character = characters.get(selected_character_index[0])
        username = username_entry.get()

        # Atualiza a coluna "personagem" com o personagem escolhido
        cursor.execute("UPDATE rpg_login SET personagem = %s WHERE user = %s", (selected_character, username))
        db_connection.commit()
        messagebox.showinfo("Sucesso", f"Personagem '{selected_character}' escolhido.")
        show_game_window()
    else:
        messagebox.showerror("Erro", "Selecione um personagem.")

# Criação da janela de registro e login
window = tk.Tk()
window.title("BSL - RPG Login")

# URL da imagem de fundo
background_url = "https://cdn.discordapp.com/attachments/1125361912113279027/1129017477226045440/NC_767-classes-rpg-WALLPAPER.png"


# Faz o download da imagem
response = requests.get(background_url)
with open("background.png", "wb") as f:
    f.write(response.content)

# Carrega a imagem de fundo
background_image = Image.open("background.png")
background_photo = ImageTk.PhotoImage(background_image)

# Cria um rótulo para exibir a imagem de fundo
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Estilo para os botões e campos
style = ttk.Style()
style.configure("TButton",
                font=("Arial", 14, "bold"),
                foreground="black",
                background="#6C63FF",
                relief="flat")
style.map("TButton",
          foreground=[("active", "black")],
          background=[("active", "#554EDA")])
style.configure("TEntry",
                font=("Arial", 14),
                relief="solid")

# Labels
username_label = tk.Label(window, text="Usuário:", font=("Arial", 14))
username_label.place(relx=0.5, rely=0.44, anchor="center")

username_entry = ttk.Entry(window)
username_entry.place(relx=0.5, rely=0.49, anchor="center")

password_label = tk.Label(window, text="Senha:", font=("Arial", 14))
password_label.place(relx=0.5, rely=0.54, anchor="center")

password_entry = ttk.Entry(window, show="*")
password_entry.place(relx=0.5, rely=0.59, anchor="center")

# Botões
register_button = ttk.Button(window, text="Registrar", command=register_user, style="TButton")
register_button.place(relx=0.45, rely=0.65, anchor="center")

login_button = ttk.Button(window, text="Login", command=login_user, style="TButton")
login_button.place(relx=0.55, rely=0.65, anchor="center")

# Definir a resolução da janela em Full HD
window_width = 1920
window_height = 1080

# Obter as dimensões da tela
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calcular a posição da janela no centro da tela
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Definir a geometria da janela para Full HD e centralizá-la
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

personagens = [
    {"nome": "Guerreiro", "Força": 10, "Defesa": 8, "Velocidade": 5, "Esquiva": 3, "Alcance": 1},
    {"nome": "Mago", "Força": 3, "Defesa": 4, "Velocidade": 10, "Esquiva": 6, "Alcance": 6},
    {"nome": "Arqueiro", "Força": 6, "Defesa": 4, "Velocidade": 8, "Esquiva": 4, "Alcance": 10},
    {"nome": "Ladrão", "Força": 5, "Defesa": 3, "Velocidade": 9, "Esquiva": 3, "Alcance": 4},
    {"nome": "Cavaleiro", "Força": 9, "Defesa": 10, "Velocidade": 3, "Esquiva": 8, "Alcance": 1},
    {"nome": "Feiticeiro", "Força": 2, "Defesa": 3, "Velocidade": 10, "Esquiva": 4, "Alcance": 8},
    {"nome": "Bárbaro", "Força": 8, "Defesa": 6, "Velocidade": 7, "Esquiva": 3, "Alcance": 1},
    {"nome": "Caçador", "Força": 6, "Defesa": 5, "Velocidade": 8, "Esquiva": 4, "Alcance": 8},
    {"nome": "Assassino", "Força": 7, "Defesa": 4, "Velocidade": 9, "Esquiva": 3, "Alcance": 4},
    {"nome": "Paladino", "Força": 7, "Defesa": 9, "Velocidade": 5, "Esquiva": 8, "Alcance": 1}
]

itens_arma = [
    {"index": 1, "nome": "Espada Longa", "Defesa": 0, "Velocidade": 10, "Esquiva": 0, "Alcance": 1},
    {"index": 2, "nome": "Machado de Batalha", "Defesa": 0, "Velocidade": 12, "Esquiva": 0, "Alcance": 1},
    {"index": 3, "nome": "Arco Longo", "Defesa": 0, "Velocidade": 8, "Esquiva": 0, "Alcance": 10},
    {"index": 4, "nome": "Cajado Mágico", "Defesa": 0, "Velocidade": 6, "Esquiva": 0, "Alcance": 8},
    {"index": 5, "nome": "Adaga Envenenada", "Defesa": 0, "Velocidade": 9, "Esquiva": 0, "Alcance": 4},
    {"index": 6, "nome": "Foice Sombria", "Defesa": 0, "Velocidade": 11, "Esquiva": 0, "Alcance": 1},
    {"index": 7, "nome": "Besta de Mão", "Defesa": 0, "Velocidade": 7, "Esquiva": 0, "Alcance": 8},
    {"index": 8, "nome": "Espada Flamejante", "Defesa": 0, "Velocidade": 14, "Esquiva": 0, "Alcance": 1},
    {"index": 9, "nome": "Arco Élfico", "Defesa": 0, "Velocidade": 9, "Esquiva": 0, "Alcance": 10},
    {"index": 10, "nome": "Varinha de Raio", "Defesa": 0, "Velocidade": 7, "Esquiva": 0, "Alcance": 8}
]

itens_escudo = [
    {"index": 11, "nome": "Escudo de Ferro", "Defesa": 8, "Velocidade": 0, "Esquiva": 5, "Alcance": 0},
    {"index": 12, "nome": "Escudo de Madeira", "Defesa": 6, "Velocidade": 0, "Esquiva": 4, "Alcance": 0},
    {"index": 13, "nome": "Escudo de Aço", "Defesa": 10, "Velocidade": 0, "Esquiva": 7, "Alcance": 0},
    {"index": 14, "nome": "Escudo de Bronze", "Defesa": 9, "Velocidade": 0, "Esquiva": 6, "Alcance": 0},
    {"index": 15, "nome": "Escudo Sagrado", "Defesa": 12, "Velocidade": 0, "Esquiva": 8, "Alcance": 0},
    {"index": 16, "nome": "Escudo de Diamante", "Defesa": 15, "Velocidade": 0, "Esquiva": 10, "Alcance": 0},
    {"index": 17, "nome": "Escudo do Dragão", "Defesa": 18, "Velocidade": 0, "Esquiva": 12, "Alcance": 0},
    {"index": 18, "nome": "Escudo de Gelo", "Defesa": 14, "Velocidade": 0, "Esquiva": 9, "Alcance": 0},
    {"index": 19, "nome": "Escudo de Fogo", "Defesa": 16, "Velocidade": 0, "Esquiva": 11, "Alcance": 0},
    {"index": 20, "nome": "Escudo Mágico", "Defesa": 20, "Velocidade": 0, "Esquiva": 15, "Alcance": 0}
]

itens_armadura = [
    {"index": 21, "nome": "Armadura de Couro", "Defesa": 5, "Velocidade": 0, "Esquiva": 3, "Alcance": 0},
    {"index": 22, "nome": "Armadura de Aço", "Defesa": 8, "Velocidade": 0, "Esquiva": 5, "Alcance": 0},
    {"index": 23, "nome": "Armadura de Placas", "Defesa": 12, "Velocidade": 0, "Esquiva": 8, "Alcance": 0},
    {"index": 24, "nome": "Armadura de Malha", "Defesa": 10, "Velocidade": 0, "Esquiva": 7, "Alcance": 0},
    {"index": 25, "nome": "Armadura Élfica", "Defesa": 15, "Velocidade": 0, "Esquiva": 10, "Alcance": 0},
    {"index": 26, "nome": "Armadura de Dragão", "Defesa": 20, "Velocidade": 0, "Esquiva": 15, "Alcance": 0},
    {"index": 27, "nome": "Armadura de Mithril", "Defesa": 18, "Velocidade": 0, "Esquiva": 12, "Alcance": 0},
    {"index": 28, "nome": "Armadura de Ouro", "Defesa": 25, "Velocidade": 0, "Esquiva": 18, "Alcance": 0},
    {"index": 29, "nome": "Armadura de Cristal", "Defesa": 22, "Velocidade": 0, "Esquiva": 16, "Alcance": 0},
    {"index": 30, "nome": "Armadura Sagrada", "Defesa": 30, "Velocidade": 0, "Esquiva": 20, "Alcance": 0}
]

itens_joia = [
    {"index": 31, "nome": "Anel da Força", "Defesa": 0, "Velocidade": 5, "Esquiva": 0, "Alcance": 0},
    {"index": 32, "nome": "Colar da Proteção", "Defesa": 3, "Velocidade": 0, "Esquiva": 5, "Alcance": 0},
    {"index": 33, "nome": "Bracelete do Poder", "Defesa": 0, "Velocidade": 8, "Esquiva": 0, "Alcance": 0},
    {"index": 34, "nome": "Amuleto da Agilidade", "Defesa": 0, "Velocidade": 6, "Esquiva": 0, "Alcance": 0},
    {"index": 35, "nome": "Anel do Encantamento", "Defesa": 0, "Velocidade": 10, "Esquiva": 0, "Alcance": 0},
    {"index": 36, "nome": "Bracelete da Cura", "Defesa": 0, "Velocidade": 4, "Esquiva": 0, "Alcance": 0},
    {"index": 37, "nome": "Colar da Sabedoria", "Defesa": 5, "Velocidade": 0, "Esquiva": 3, "Alcance": 0},
    {"index": 38, "nome": "Anel da Sorte", "Defesa": 0, "Velocidade": 4, "Esquiva": 0, "Alcance": 0},
    {"index": 39, "nome": "Amuleto do Conhecimento", "Defesa": 0, "Velocidade": 7, "Esquiva": 0, "Alcance": 0},
    {"index": 40, "nome": "Bracelete da Resistência", "Defesa": 6, "Velocidade": 0, "Esquiva": 4, "Alcance": 0}
]

def show_game_window():
    #close_window_by_title("BSL - RPG Login")
    game_window = tk.Toplevel()
    game_window.title("BSL - RPG GAME")

    # URL da imagem de fundo
    background_url2 = "https://cdn.discordapp.com/attachments/1125361912113279027/1129059720192344185/Default_elf_warrior_man_short_blonde_hair_with_blue_eyes_sword_0_c8636bd5-67b0-44cc-b180-a4a7b3ac66b0_1.jpg"

    # Faz o download da imagem
    response = requests.get(background_url2)
    with open("background2.png", "wb") as f:
        f.write(response.content)

    # Carrega a imagem de fundo
    background_image = Image.open("background2.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Cria um rótulo para exibir a imagem de fundo
    background_label = tk.Label(game_window, image=background_photo)
    background_label.image = background_photo  # Mantém uma referência à imagem

    # Definir a resolução da janela em Full HD
    window_width = 1920
    window_height = 1080

    # Obter as dimensões da tela
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()

    # Calcular a posição da janela no centro da tela
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Definir a geometria da janela para Full HD e centralizá-la
    game_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Exibe as informações do personagem
    username = username_entry.get()

    # Obtém as informações do personagem do banco de dados
    cursor.execute("SELECT personagem, nivel, money, arma, escudo, armadura, joia FROM rpg_login WHERE user = %s", (username,))
    result = cursor.fetchone()

    if result is not None:
        character_name = result[0]
        character_level = result[1]
        character_money = result[2]
        equipped_weapon_index = result[3]
        equipped_shield_index = result[4]
        equipped_armor_index = result[5]
        equipped_jewel_index = result[6]

        character_label = tk.Label(game_window, text=f"Personagem: {character_name}", font=("Arial", 16), bg="white")
        character_label.pack(anchor="w")  # Alinha à esquerda

        level_label = tk.Label(game_window, text=f"Nível: {character_level}", font=("Arial", 16), bg="white")
        level_label.pack(anchor="w")  # Alinha à esquerda

        money_label = tk.Label(game_window, text=f"Dinheiro: {character_money}", font=("Arial", 16), bg="white")
        money_label.pack(anchor="w")  # Alinha à esquerda

        items_frame = tk.Frame(game_window, bg="white")
        items_frame.pack(anchor="w")  # Alinha à esquerda

        # Labels dos itens
        weapon_label = tk.Label(items_frame, text="Arma:", font=("Arial", 16), bg="white")
        weapon_label.grid(row=0, column=0, sticky="e")
        shield_label = tk.Label(items_frame, text="Escudo:", font=("Arial", 16), bg="white")
        shield_label.grid(row=1, column=0, sticky="e")
        armor_label = tk.Label(items_frame, text="Armadura:", font=("Arial", 16), bg="white")
        armor_label.grid(row=2, column=0, sticky="e")
        jewel_label = tk.Label(items_frame, text="Joia:", font=("Arial", 16), bg="white")
        jewel_label.grid(row=3, column=0, sticky="e")
    
        # Obtém os nomes dos itens equipados
        equipped_weapon_name = next((item["nome"] for item in itens_arma if item["index"] == equipped_weapon_index), "")
        equipped_shield_name = next((item["nome"] for item in itens_escudo if item["index"] == equipped_shield_index), "")
        equipped_armor_name = next((item["nome"] for item in itens_armadura if item["index"] == equipped_armor_index), "")
        equipped_jewel_name = next((item["nome"] for item in itens_joia if item["index"] == equipped_jewel_index), "")
    
        # Labels dos nomes dos itens
        equipped_weapon_label = tk.Label(items_frame, text=equipped_weapon_name, font=("Arial", 16), bg="white")
        equipped_weapon_label.grid(row=0, column=1, sticky="w")
        equipped_shield_label = tk.Label(items_frame, text=equipped_shield_name, font=("Arial", 16), bg="white")
        equipped_shield_label.grid(row=1, column=1, sticky="w")
        equipped_armor_label = tk.Label(items_frame, text=equipped_armor_name, font=("Arial", 16), bg="white")
        equipped_armor_label.grid(row=2, column=1, sticky="w")
        equipped_jewel_label = tk.Label(items_frame, text=equipped_jewel_name, font=("Arial", 16), bg="white")
        equipped_jewel_label.grid(row=3, column=1, sticky="w")

        character_index = next((index for index, character in enumerate(personagens) if character["nome"] == character_name), None)
        # Aumenta os atributos em 10% a cada nível
        level_multiplier = 0.25 * character_level
    
        character_attributes = personagens[character_index].copy() if character_index is not None else None
        if character_attributes is not None:
            # Multiplica os valores dos atributos pelo multiplicador de nível
            for attribute in character_attributes:
                if attribute != "nome":
                    character_attributes[attribute] = int(character_attributes[attribute] + level_multiplier)


        if character_attributes is not None:
            # Obtém os atributos adicionais dos itens equipados
            if equipped_weapon_index > 0:
                weapon_attributes = next((item for item in itens_arma if item['index'] == equipped_weapon_index), None)
                if weapon_attributes is not None:
                    for attribute in weapon_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += weapon_attributes[attribute]

            if equipped_shield_index > 0:
                shield_attributes = next((item for item in itens_escudo if item['index'] == equipped_shield_index), None)
                if shield_attributes is not None:
                    for attribute in shield_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += shield_attributes[attribute]
            
            if equipped_armor_index > 0:
                armor_attributes = next((item for item in itens_armadura if item['index'] == equipped_armor_index), None)
                if armor_attributes is not None:
                    for attribute in armor_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += armor_attributes[attribute]

            if equipped_jewel_index > 0:
                jewel_attributes = next((item for item in itens_joia if item['index'] == equipped_jewel_index), None)
                if jewel_attributes is not None:
                    for attribute in jewel_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += jewel_attributes[attribute]

            # Exibe os valores dos atributos do personagem
            for i, attribute in enumerate(character_attributes):
                if attribute == "nome":
                    continue  # Pula o atributo "nome"
                attribute_label = tk.Label(items_frame, text=f"{attribute.capitalize()}: {character_attributes[attribute]}", font=("Arial", 16), bg="white")
                attribute_label.grid(row=i + 4, column=0, sticky="e", pady=5, padx=10)
        else:
            messagebox.showerror("Erro", "Personagem não encontrado.")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

    # Atualizar a janela do jogo para exibir o rótulo e a imagem de fundo corretamente
    game_window.update()
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Botão para ir para a janela do mundo
    world_button = ttk.Button(game_window, text="Ir para o Mundo", command=show_world_window, style="TButton")
    world_button.pack(anchor="w")  # Alinha à esquerda


def show_world_window():
    world_window = tk.Toplevel()
    world_window.title("BSL - RPG GAME - Mundo")

    # URL da imagem de fundo
    background_url = "https://cdn.discordapp.com/attachments/1125361912113279027/1129100573313085532/Default_A_detailed_map_of_a_fantastical_world_filled_with_myth_0_ec0f0186-6bf1-4ffb-b074-589c3be8f633_1.jpg"

    # Faz o download da imagem
    response = requests.get(background_url)
    with open("background_map.png", "wb") as f:
        f.write(response.content)

    # Carrega a imagem de fundo
    background_image = Image.open("background_map.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Cria um rótulo para exibir a imagem de fundo
    background_label = tk.Label(world_window, image=background_photo)
    background_label.image = background_photo  # Mantém uma referência à imagem
    background_label.pack()

    # Botões
    button1 = ttk.Button(world_window, text="Botão 1", command=funcao_botao1, style="TButton")
    button1.place(x=30, y=980)

    button2 = ttk.Button(world_window, text="Botão 2", command=funcao_botao2, style="TButton")
    button2.place(x=1250, y=300)

    button3 = ttk.Button(world_window, text="PVP", command=funcao_botao3, style="TButton")
    button3.place(x=300, y=450)

    button4 = ttk.Button(world_window, text="Botão 4", command=funcao_botao4, style="TButton")
    button4.place(x=620, y=420)

    button5 = ttk.Button(world_window, text="Botão 5", command=funcao_botao5, style="TButton")
    button5.place(x=800, y=750)

    # Atualizar a janela do mundo para exibir o rótulo e a imagem de fundo corretamente
    world_window.update()
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Executar o loop de eventos da janela
    world_window.mainloop()


def funcao_botao1():
    # Implemente a ação do Botão 1 aqui
    pass


def funcao_botao2():
    # Implemente a ação do Botão 2 aqui
    pass

def calculate_attribute_score(attributes):
    # Exibe as informações do personagem
    username = username_entry.get()

    # Obtém as informações do personagem do banco de dados
    cursor.execute("SELECT personagem, nivel, money, arma, escudo, armadura, joia FROM rpg_login WHERE user = %s", (username,))
    result = cursor.fetchone()

    if result is not None:
        character_name = result[0]
        character_level = result[1]
        equipped_weapon_index = result[3]
        equipped_shield_index = result[4]
        equipped_armor_index = result[5]
        equipped_jewel_index = result[6]

        character_index = next((index for index, character in enumerate(personagens) if character["nome"] == character_name), None)
        # Aumenta os atributos em 10% a cada nível
        level_multiplier = 0.25 * character_level
    
        character_attributes = personagens[character_index].copy() if character_index is not None else None
        if character_attributes is not None:
            # Multiplica os valores dos atributos pelo multiplicador de nível
            for attribute in character_attributes:
                if attribute != "nome":
                    character_attributes[attribute] = int(character_attributes[attribute] + level_multiplier)

        if character_attributes is not None:
            # Obtém os atributos adicionais dos itens equipados
            if equipped_weapon_index > 0:
                weapon_attributes = next((item for item in itens_arma if item['index'] == equipped_weapon_index), None)
                if weapon_attributes is not None:
                    for attribute in weapon_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += weapon_attributes[attribute]

            if equipped_shield_index > 0:
                shield_attributes = next((item for item in itens_escudo if item['index'] == equipped_shield_index), None)
                if shield_attributes is not None:
                    for attribute in shield_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += shield_attributes[attribute]
            
            if equipped_armor_index > 0:
                armor_attributes = next((item for item in itens_armadura if item['index'] == equipped_armor_index), None)
                if armor_attributes is not None:
                    for attribute in armor_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += armor_attributes[attribute]

            if equipped_jewel_index > 0:
                jewel_attributes = next((item for item in itens_joia if item['index'] == equipped_jewel_index), None)
                if jewel_attributes is not None:
                    for attribute in jewel_attributes:
                        if attribute not in character_attributes:
                            character_attributes[attribute] = 0
                        character_attributes[attribute] += jewel_attributes[attribute]

            # Exibe os valores dos atributos do personagem
            for i, attribute in enumerate(character_attributes):
                if attribute == "nome":
                    continue  # Pula o atributo "nome"
        else:
            messagebox.showerror("Erro", "Personagem não encontrado.")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

    # Calcula a pontuação do atributo
    score = 0
    for value in attributes.values():
        if isinstance(value, (int, float)):
            score += value

    return score



def funcao_botao3():
    # Obtém o nome de usuário do jogador atual
    username = username_entry.get()

    # Verifica se o nome de usuário é válido
    if not username:
        messagebox.showerror("Erro", "Por favor, insira um nome de usuário.")
        return

    # Seleciona outro jogador aleatório da base de dados
    cursor.execute("SELECT user FROM rpg_login WHERE user != %s ORDER BY RAND() LIMIT 1", (username,))
    opponent = cursor.fetchone()

    if opponent is None:
        messagebox.showerror("Erro", "Nenhum oponente disponível.")
        return

    # Obtém os atributos do jogador atual do banco de dados
    cursor.execute("SELECT personagem, nivel, arma, escudo, armadura, joia FROM rpg_login WHERE user = %s", (username,))
    player_result = cursor.fetchone()

    if player_result is None:
        messagebox.showerror("Erro", "Jogador não encontrado.")
        return

    # Obtém os atributos do oponente do banco de dados
    cursor.execute("SELECT personagem, nivel, arma, escudo, armadura, joia FROM rpg_login WHERE user = %s", (opponent[0],))
    opponent_result = cursor.fetchone()

    if opponent_result is None:
        messagebox.showerror("Erro", "Oponente não encontrado.")
        return

    # Extrai os atributos do jogador atual
    player_attributes = {}
    player_attributes["personagem"] = player_result[0]
    player_attributes["nivel"] = player_result[1]
    player_attributes["arma"] = player_result[2]
    player_attributes["escudo"] = player_result[3]
    player_attributes["armadura"] = player_result[4]
    player_attributes["joia"] = player_result[5]

    # Extrai os atributos do oponente
    opponent_attributes = {}
    opponent_attributes["personagem"] = opponent_result[0]
    opponent_attributes["nivel"] = opponent_result[1]
    opponent_attributes["arma"] = opponent_result[2]
    opponent_attributes["escudo"] = opponent_result[3]
    opponent_attributes["armadura"] = opponent_result[4]
    opponent_attributes["joia"] = opponent_result[5]

    # Realiza o cálculo de atributos para determinar o vencedor
    player_score = calculate_attribute_score(player_attributes)
    opponent_score = calculate_attribute_score(opponent_attributes)

    # Cria a janela de batalha
    battle_window = tk.Toplevel()
    battle_window.title("Batalha PvP")

    # Implemente o layout da janela de batalha e exiba as informações dos jogadores

    # Exemplo de layout básico:
    player_label = tk.Label(battle_window, text=f"Jogador: {player_attributes['personagem']}")
    player_label.pack()

    opponent_label = tk.Label(battle_window, text=f"Oponente: {opponent_attributes['personagem']}")
    opponent_label.pack()

    # Exiba os atributos e scores dos jogadores

    # Exemplo:
    player_attributes_label = tk.Label(battle_window, text=f"Atributos do Jogador: {player_attributes}")
    player_attributes_label.pack()

    opponent_attributes_label = tk.Label(battle_window, text=f"Atributos do Oponente: {opponent_attributes}")
    opponent_attributes_label.pack()

    player_score_label = tk.Label(battle_window, text=f"Score do Jogador: {player_score}")
    player_score_label.pack()

    opponent_score_label = tk.Label(battle_window, text=f"Score do Oponente: {opponent_score}")
    opponent_score_label.pack()

    # Implemente a lógica da batalha e exiba os resultados

    # Exemplo:
    if player_score > opponent_score:
        result_label = tk.Label(battle_window, text="Jogador venceu a batalha!")
    elif player_score < opponent_score:
        result_label = tk.Label(battle_window, text="Oponente venceu a batalha!")
    else:
        result_label = tk.Label(battle_window, text="A batalha terminou em empate!")

    result_label.pack()




def funcao_botao4():
    # Implemente a ação do Botão 4 aqui
    pass


def funcao_botao5():
    # Implemente a ação do Botão 5 aqui
    pass

def close_window_by_title(title):
    # Percorre todas as janelas abertas
    for window in tk.Toplevel.winfo_children(tk._default_root):
        # Verifica se o título da janela corresponde ao título desejado
        if window.winfo_toplevel().title() == title:
            window.winfo_toplevel().destroy()
            break

    #fecha janela, ex: #close_window_by_title("BSL - RPG Login")


# Conexão com o banco de dados
db_connection = mysql.connector.connect(
    host='',
    user='',
    password='',
    database=''
)
cursor = db_connection.cursor()

# Inicia a interface
window.mainloop()
