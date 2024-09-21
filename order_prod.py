from dataclasses import dataclass, asdict

@dataclass
class OrdemDeProducao:
    # Atributos Principais
    dataEntrega: str #1 td
    codigoOrdemProducao: str #2 td
    cliente: str #3 td
    codigoMaterial: str #4 td
    descricaoMaterial: str #5 td
    quantidade: int # 6 td
    nfes: list[int]
    
class OrdensDeProducao:
    # Atributo de classe para armazenar a lista de dicionários
    instances: dict[str, str] = {}

    @classmethod
    def create(cls, dataEntrega: str, codigoOrdemProducao: str, cliente: str, codigoMaterial: str, descricaoMaterial: str, quantidade: int, nfes: list[int]) -> None:
        # Cria uma nova instância de OP
        instance = OrdemDeProducao(dataEntrega, codigoOrdemProducao, cliente, codigoMaterial, descricaoMaterial, quantidade, nfes)
        cls.instances[instance.codigoOrdemProducao] = asdict(instance)

    @classmethod
    def get_instances(cls) -> "OrdensDeProducao":
        return cls.instances

    @classmethod
    def find_by_codigo(cls, codigo) -> dict[str, str]:
        return cls.instances.get(codigo, None)