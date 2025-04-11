class GeneralLFSR:
    def __init__(self, size=4, initial_state=None, tap_sequence=None):
        """
        Inisialisasi LFSR yang bisa dikonfigurasi

        Parameters:
        - size: Ukuran register
        - initial_state: List bit awal
        - tap_sequence: List indeks bit untuk feedback
        """
        self.size = size

        # Set state awal
        if initial_state is None:
            self.state = [0] * size
        else:
            if len(initial_state) != size:
                raise ValueError(f"Panjang state awal harus {size} bit")
            if any(bit not in (0, 1) for bit in initial_state):
                raise ValueError("State hanya boleh berisi 0 atau 1")
            self.state = initial_state.copy()

        # Set tap sequence
        if tap_sequence is None:
            self.tap_sequence = [size - 1, size - 2]  # Default: dua bit paling kanan
        else:
            if any(tap >= size for tap in tap_sequence):
                raise ValueError("Indeks tap melebihi ukuran register")
            self.tap_sequence = tap_sequence.copy()

    def get_current_state(self):
        """Mengembalikan state saat ini"""
        return ''.join(str(bit) for bit in self.state)

    def set_state(self, new_state):
        """Mengubah state register"""
        if len(new_state) != self.size:
            raise ValueError(f"Panjang state baru harus {self.size} bit")
        if any(bit not in (0, 1) for bit in new_state):
            raise ValueError("State hanya boleh berisi 0 atau 1")
        self.state = new_state.copy()

    def get_next_bit(self):
        """Menghasilkan bit berikutnya dan mengupdate state"""
        feedback = 0
        for tap in self.tap_sequence:
            feedback ^= self.state[tap]

        next_bit = self.state[0]  # Output bit paling kiri

        # Geser semua bit ke kiri
        for i in range(self.size - 1):
            self.state[i] = self.state[i + 1]

        # Masukkan feedback ke bit paling kanan
        self.state[-1] = feedback

        return next_bit

    def reset(self):
        """Reset register ke state awal (semua 0)"""
        self.state = [0] * self.size


def simulate_general(size=4, initial_state='0110', taps='3,2', steps=20):
    """Fungsi untuk General LFSR"""
    # Konversi parameter input
    init_state = [int(bit) for bit in initial_state]
    tap_sequence = [int(tap) for tap in taps.split(',')]

    # Inisialisasi LFSR
    lfsr = GeneralLFSR(
        size=size,
        initial_state=init_state,
        tap_sequence=tap_sequence
    )

    print("\nSimulasi General LFSR")
    print("=" * 60)
    print(f"Konfigurasi: Size={size}, Initial State={init_state}, Taps={tap_sequence}")
    print("t | State      | Output | State (bin)")
    print("-" * 60)

    for t in range(steps):
        current_state = lfsr.state.copy()
        output_bit = lfsr.get_next_bit()

        state_bin = lfsr.get_current_state()
        state_str = ' '.join(str(bit) for bit in current_state)

        print(f"{t:2} | {state_str:10} |   {output_bit}    | {state_bin}")


if __name__ == "__main__":
    simulate_general()