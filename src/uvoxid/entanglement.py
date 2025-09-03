import random
from typing import List, Dict, Set

class EntanglementEngine:
    def __init__(self):
        # Registry: entanglement_id → set of voxel ints
        self.entangled_groups: Dict[int, Set[int]] = {}
        self.next_id = 1

    def entangle(self, voxels: List[int], n_bits: int) -> int:
        """
        Entangle a group of voxels by forcing them to share last n_bits.
        Returns entanglement group ID.
        """
        mask = (1 << n_bits) - 1
        # Use the first voxel as reference suffix
        ref_suffix = voxels[0] & mask

        entangled = set()
        for v in voxels:
            v = (v & ~mask) | ref_suffix
            entangled.add(v)

        group_id = self.next_id
        self.next_id += 1
        self.entangled_groups[group_id] = entangled
        return group_id

    def collapse(self, group_id: int, n_bits: int) -> Set[int]:
        """
        Collapse all voxels in a group to a new random suffix.
        Returns updated set of voxels.
        """
        if group_id not in self.entangled_groups:
            raise ValueError(f"No such entangled group {group_id}")

        mask = (1 << n_bits) - 1
        new_suffix = random.getrandbits(n_bits)

        updated = set()
        for v in self.entangled_groups[group_id]:
            collapsed = (v & ~mask) | new_suffix
            updated.add(collapsed)

        self.entangled_groups[group_id] = updated
        return updated

    def get_group(self, group_id: int) -> Set[int]:
        return self.entangled_groups.get(group_id, set())
