from dataclasses import dataclass, asdict
import json

@dataclass
class OrdemDeProducao:
    # Atributos Principais
    dataEntrega: str #1 td
    codigoOrdemProducao: int #2 td
    cliente: str #3 td
    codigoMaterial: str #4 td
    descricaoMaterial: str #5 td
    quantidade: int # 6 td
    nfes: list[int]
    
class OrdensDeProducao:
    # Atributo de classe para armazenar a lista de dicionários
    instances: dict[str, dict] = {}

    @classmethod
    def create(cls, dataEntrega: str, codigoOrdemProducao: int, cliente: str, codigoMaterial: str, descricaoMaterial: str, quantidade: int, nfes: list[int]) -> None:
        # Cria uma nova instância de OP
        instance = OrdemDeProducao(dataEntrega, codigoOrdemProducao, cliente, codigoMaterial, descricaoMaterial, quantidade, nfes)
        cls.instances[instance.codigoOrdemProducao] = asdict(instance)

    @classmethod
    def get_instances(cls) -> "OrdensDeProducao":
        return cls.instances

    @classmethod
    def find_by_codigo(cls, codigo) -> dict[int, int]:
        return cls.instances.get(codigo, None)
    
    @classmethod
    def to_json(cls):
        return json.dumps({"ordensDeProducao": cls.instances}, indent=4, ensure_ascii=False)
    
    @classmethod
    def save_json_file(cls, file_name: str = "ordens_de_producao.json"):
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump({"ordensDeProducao": cls.instances}, file, indent=4, ensure_ascii=False)