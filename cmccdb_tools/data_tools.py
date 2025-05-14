

import rdkit.Chem
from rdkit.Chem import Descriptors

__all__ = [
    "parse_mol",
    "compute_component_mass"
]
def parse_mol(smiles):
    mol = rdkit.Chem.MolFromSmiles(smiles)
    mol = rdkit.Chem.AddHs(mol)
    return mol

def compute_component_mass(smiles):
    return Descriptors.ExactMolWt(parse_mol(smiles))