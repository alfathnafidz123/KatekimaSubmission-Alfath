class BasicLFSR:
    def __init__(self, initial_state=[0, 1, 1, 0]):
        #Inisialisasi LFSR dengan state awal tetap Default: [0, 1, 1, 0] sesuai soal

        if len(initial_state) != 4:
            raise ValueError("State awal harus 4 bit")
        if any(bit not in (0, 1) for bit in initial_state):
            raise ValueError("State hanya boleh berisi 0 atau 1")

        self.state = initial_state.copy()
        self.initial_state = initial_state.copy()

    def get_current_state(self):
        # Return state saat ini sebagai string
        return ''.join(str(bit) for bit in self.state)

    def get_next_bit(self):

        #Menghasilkan bit berikutnya dan mengupdate state menggunakan XOR antara bit 3 dan 2

        feedback = self.state[3] ^ self.state[2]  # XOR bit 3 dan 2
        next_bit = self.state[0]  # Output bit paling kiri

        # Geser semua bit ke kiri
        for i in range(len(self.state) - 1):
            self.state[i] = self.state[i + 1]

        # Masukkan feedback ke bit paling kanan
        self.state[-1] = feedback

        return next_bit

    def reset(self):
        # Reset ke state awal
        self.state = self.initial_state.copy()


def simulate_basic(steps=20):
    lfsr = BasicLFSR()

    # Data expected untuk validasi (16 state pertama dari contoh soal)
    expected_states = [
        '0110', '0011', '1001', '0100',
        '0010', '0001', '1000', '1100',
        '1110', '1111', '0111', '1011',
        '0101', '1010', '1101', '0110'
    ]

    print("\nSimulasi Basic LFSR")
    print("=" * 50)
    print("t | State | Output | Confirmation")
    print("-" * 50)

    for t in range(steps):
        current_state = lfsr.get_current_state()
        output_bit = lfsr.get_next_bit()

        # Confirmation
        validation = ""
        if t < 16:
            if current_state == expected_states[t]:
                validation = ""
            else:
                validation = f" expected ({expected_states[t]})"

        print(f"{t:2} | {current_state} |   {output_bit}    | {validation}")


if __name__ == "__main__":
    simulate_basic()