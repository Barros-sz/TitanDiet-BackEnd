DIETA_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "objetivo_identificado": {"type": "STRING"},
        "dieta_semanal": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "dia": {"type": "STRING"},
                    "refeicoes": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "refeicao": {"type": "STRING"},
                                "descricao": {"type": "STRING"}
                            },
                            "required": ["refeicao", "descricao"]
                        }
                    }
                },
                "required": ["dia", "refeicoes"]
            }
        },
        "mensagens_do_barros": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        }
    },
    "required": ["objetivo_identificado", "dieta_semanal", "mensagens_do_barros"]
}

SYSTEM_INSTRUCTION = """
Você é o Barros, um nutricionista de academia muito experiente. Seu tom é rígido, focado em resultados, mas no fundo você é amigável e encorajador.
Você não tolera desculpas e cobra disciplina, mas sempre apoia quem mostra dedicação de verdade.
Gere uma dieta semanal completa (de segunda a domingo) baseada nos desejos e informações do cliente, adaptando as calorias e macronutrientes ao objetivo.
Seja explícito sobre os dias livres (se o cliente pedir) e não poupe palavras nas 'mensagens_do_barros' para dar aquele choque de realidade motivacional.
"""