class AppError(Exception):
    """
    Base para todos os erros que queremos devolver ao utilizador de forma controlada.

    Cada subclasse define:
      - status_code: o código HTTP da resposta
      - code: um identificador estável que o frontend pode usar (não muda se a mensagem mudar)
      - message: texto legível para o utilizador
    """

    status_code: int = 500
    code: str = "internal_error"
    message: str = "Ocorreu um erro inesperado."

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class ShortCodeGenerationError(AppError):
    status_code = 503
    code = "short_code_generation_failed"
    message = "Não foi possível gerar um código curto. Tenta novamente."


class InvalidUrlError(AppError):
    status_code = 422
    code = "invalid_url"
    message = "URL inválida. Usa um endereço completo começado por http:// ou https://."
