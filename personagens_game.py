import random


class Ser:
    def __init__(self, nome: str, level: int, vida: int):
        self.nome = nome
        self.level = level
        self.vida = vida

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def receber_dano(self, dano: int) -> None:
        self.vida = max(0, self.vida - dano)

    def atacar(self, alvo: "Ser") -> int:
        dano = random.randint(max(1, self.level), self.level * 3)
        alvo.receber_dano(dano)
        return dano


class Humano(Ser):
    def __init__(self, nome: str):
        super().__init__(nome=nome, level=1, vida=100)
        self.xp = 0

    def xp_para_proximo_level(self) -> int:
        return 100 * self.level

    def ganhar_xp(self, ganho: int) -> None:
        self.xp += ganho
        while self.xp >= self.xp_para_proximo_level():
            self.xp -= self.xp_para_proximo_level()
            self.level += 1
            self.vida += 20
            print(f"\n⭐ Level Up! Agora você está no nível {self.level}.")

    def ataque_especial(self, alvo: Ser) -> int:
        dano = random.randint(self.level * 3, self.level * 5)
        alvo.receber_dano(dano)
        return dano


class Monstro(Ser):
    def __init__(self, nome: str, level: int, vida: int, xp_recompensa: int):
        super().__init__(nome, level, vida)
        self.xp_recompensa = xp_recompensa


def criar_monstros() -> list[Monstro]:
    monstros_base = [
        Monstro(nome="Aranha", level=2, vida=35, xp_recompensa=40),
        Monstro(nome="Rato Gigante", level=1, vida=20, xp_recompensa=20),
        Monstro(nome="Goblin", level=3, vida=45, xp_recompensa=55),
        Monstro(nome="Slime", level=1, vida=25, xp_recompensa=25),
        Monstro(nome="Esqueleto", level=4, vida=60, xp_recompensa=70),
        Monstro(nome="Flor Venenosa", level=7, vida=130, xp_recompensa=150),
        Monstro(nome="Dragão", level=10, vida=220, xp_recompensa=300),
        Monstro(nome="Panda Kung Fu", level=150, vida=2220, xp_recompensa=3000),
        Monstro(nome="Mickey Mouse", level=100, vida=1500, xp_recompensa=2000),
        Monstro(nome="Dragão Branco de 3 cabeças", level=200, vida=5000, xp_recompensa=5000),
        Monstro(nome="Dragão Conspirador", level=200, vida=6000, xp_recompensa=7000),
        Monstro(nome="Bolsonaro", level=2, vida=20, xp_recompensa=30),
    ]

    adjetivos = [
        "Sombrio",
        "Ancestral",
        "Sanguinário",
        "Arcano",
        "Abissal",
        "Tempestuoso",
        "Corrompido",
        "Feroz",
        "Titânico",
        "Imortal",
        "Acido",
        "Ardente",
        "Vidente",
        "Ventuoso",
    ]
    tipos = [
        "Lobo",
        "Golem",
        "Hidra",
        "Espectro",
        "Quimera",
        "Minotauro",
        "Serpente",
        "Vigia",
        "Cavaleiro",
        "Ceifador",
        "Andromeda",
        "Espadachim Noturno",
        "General",
    ]

    monstros_extras = []
    for indice, adjetivo in enumerate(adjetivos):
        for j, tipo in enumerate(tipos):
            level = ((indice * len(tipos) + j) * 17) % 200 + 1
            vida = 30 + (level * 12)
            xp_recompensa = 20 + (level * 15)
            monstros_extras.append(
                Monstro(
                    nome=f"{tipo} {adjetivo}",
                    level=level,
                    vida=vida,
                    xp_recompensa=xp_recompensa,
                )
            )

    return monstros_base + monstros_extras


def filtrar_monstros_por_nivel(heroi: Humano, monstros: list[Monstro]) -> list[Monstro]:
    """Retorna monstros com dificuldade adequada ao nível atual do herói."""
    level_minimo = max(1, heroi.level - 10)
    level_maximo = heroi.level + 4
    monstros_adequados = [
        monstro for monstro in monstros if level_minimo <= monstro.level <= level_maximo
    ]

    # Fallback de segurança caso não exista nenhum monstro no intervalo exato.
    if monstros_adequados:
        return monstros_adequados

    level_maximo_expandido = heroi.level + 6
    monstros_adequados = [
        monstro for monstro in monstros if monstro.level <= level_maximo_expandido
    ]

    return monstros_adequados if monstros_adequados else monstros


def tentar_fuga(heroi: Humano, monstro: Monstro) -> bool:
    if monstro.level >= heroi.level + 5:
        print("\nO monstro é muito forte e não deixou você fugir.")
        return False

    chance_sucesso = 70
    sorteio = random.randint(1, 100)
    if sorteio <= chance_sucesso:
        print("\nVocê conseguiu fugir!")
        return True

    print("\nVocê tentou fugir, mas o monstro te alcançou!")
    return False


def batalha(heroi: Humano, monstro: Monstro) -> bool:
    print(f"\n⚔️ Batalha iniciada: {heroi.nome} vs {monstro.nome}")

    while heroi.esta_vivo() and monstro.esta_vivo():
        print(
            f"\n{heroi.nome} | Vida: {heroi.vida} | Nível: {heroi.level} | XP: {heroi.xp}/{heroi.xp_para_proximo_level()}"
        )
        print(f"{monstro.nome} | Vida: {monstro.vida} | Nível: {monstro.level}")

        escolha = input("\nEscolha sua ação (1-Ataque normal | 2-Ataque especial): ").strip()

        if escolha == "1":
            dano = heroi.atacar(monstro)
            print(f"Você atacou e causou {dano} de dano.")
        elif escolha == "2":
            dano = heroi.ataque_especial(monstro)
            print(f"Você usou ataque especial e causou {dano} de dano.")
        else:
            print("Ação inválida. Você perdeu o turno!")

        if not monstro.esta_vivo():
            print(f"\n✅ Você derrotou {monstro.nome}!")
            heroi.ganhar_xp(monstro.xp_recompensa)
            return True

        dano_monstro = monstro.atacar(heroi)
        print(f"{monstro.nome} atacou e causou {dano_monstro} de dano.")

    print("\n❌ Você foi derrotado.")
    return False


def criar_chefao_final() -> Monstro:
    return Monstro(
        nome="Abyssal Prime, o Devorador de Mundos",
        level=260,
        vida=5000,
        xp_recompensa=10000,
    )


def main() -> None:
    print("=== Jogo de Personagens ===")
    nome = input("Digite o nome do herói: ").strip()
    heroi = Humano(nome=nome if nome else "Aventureiro")
    monstros = criar_monstros()

    while heroi.esta_vivo():
        monstros_disponiveis = filtrar_monstros_por_nivel(heroi, monstros)
        monstro = random.choice(monstros_disponiveis)
        print(f"\nUm {monstro.nome} apareceu! (Nível {monstro.level}, Vida {monstro.vida})")

        escolha = input("Deseja lutar ou fugir? (l/f): ").strip().lower()

        if escolha == "f":
            if tentar_fuga(heroi, monstro):
                continue
            venceu_luta = batalha(heroi, monstro)
        elif escolha == "l":
            venceu_luta = batalha(heroi, monstro)
        else:
            print("Opção inválida, escolha novamente.")
            continue

        if venceu_luta and monstro.level == 200:
            chefao_final = criar_chefao_final()
            print("\n🔥 Você derrotou o monstro de nível 200 e invocou o CHEFÃO FINAL! 🔥")
            venceu_chefao = batalha(heroi, chefao_final)
            if venceu_chefao:
                print("\n🏆 PARABÉNS! Você derrotou o chefão final e ZEROU o jogo!")
                print("Obrigado por jogar.")
            break

        if heroi.esta_vivo():
            continuar = input("\nDeseja continuar jogando? (s/n): ").strip().lower()
            if continuar != "s":
                break

    print("\nFim do jogo.")


if __name__ == "__main__":
    main()