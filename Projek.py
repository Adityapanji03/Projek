import os
import pandas as pd

# Nama file CSV untuk menyimpan data transaksi
namaFile = "transaksi_kasir_ayam_geprek.csv"
stok_ayam = 0
ayam_terjual = 0
harga_ayam_geprek = 15000
harga_ayam_bakar = 16000
harga_es_teh = 3000
harga_es_jeruk = 4000

nama_pelanggan = ""
tanggal = ""
nama_barang = ""
total_harga = 0

def tambahkan_transaksi():
    global nama_pelanggan, tanggal, nama_barang, total_harga
    tanggal = input("Masukkan tanggal transaksi (Tahun-Bulan-Hari): ")
    nama_pelanggan = str(input("Masukkan nama pelanggan : "))
    pesanan = []  # Membuat list untuk menyimpan pesanan dalam satu transaksi

    while True:
        # Menampilkan pilihan menu
        print("Pilih menu:")
        print("1. Ayam Geprek (Rp 15000)")
        print("2. Ayam Bakar (Rp 16000)")
        print("3. Es Teh (Rp 3000)")
        print("4. Es Jeruk (Rp 4000)")
        print("5. Selesai")

        pilihan_menu = input("Masukkan nomor menu (1/2/3/4) atau selesai (5) untuk menyelesaikan pesanan: ")

        if pilihan_menu == "5":
            break

        # Pisahkan nomor menu yang diinput
        nomor_menu = pilihan_menu.split()

        for nomor in nomor_menu:
            if nomor == '1':
                pesanan.append("Ayam Geprek")
            elif nomor == '2':
                pesanan.append("Ayam Bakar")
            elif nomor == '3':
                pesanan.append("Es Teh")
            elif nomor == '4':
                pesanan.append("Es Jeruk")
            else:
                print("Nomor menu tidak valid:", nomor)
                continue  # Lewati item yang tidak valid

    if pesanan:
        # Gabungkan semua pesanan dalam satu string dengan koma sebagai pemisah
        nama_barang = ', '.join(pesanan)
        # Hitung jumlah barang dalam pesanan
        jumlah_barang = len(pesanan)

        # Hitung total harga pesanan
        total_harga = 0
        for barang in pesanan:
            if barang == "Ayam Geprek":
                total_harga += harga_ayam_geprek
            elif barang == "Ayam Bakar":
                total_harga += harga_ayam_bakar
            elif barang == "Es Teh":
                total_harga += harga_es_teh
            elif barang == "Es Jeruk":
                total_harga += harga_es_jeruk

        print("Ringkasan Pesanan:")
        print(f"{nama_barang} (Rp {total_harga})")

        pilihan = str(input("ingin mencetak struk? (ya/tidak)"))
        if pilihan == "ya":
            print("=====Geprek Barokah=====")
            print("="*10, "Geprek Barokah", "="*10)
            print("Nama: ", nama_pelanggan)
            print("Tanggal: ", tanggal)
            print("Pesanan: ", nama_barang)
            print("Total Harga: Rp", total_harga)
            print("Terima Kasih, Jangan Lupa Mampir Kembali !")
            print("="*40)
        elif == "tidak":
            print("struk tidak dicetak")

        # Menyimpan transaksi dalam DataFrame
        transaksi = pd.DataFrame({'Tanggal': [tanggal], 'Nama Barang': [nama_barang], 'Total Harga': [total_harga]})

        if not os.path.exists(namaFile):
            transaksi.to_csv(namaFile, index=False)
        else:
            transaksi.to_csv(namaFile, mode='a', header=False, index=False)

        print()
        print("Transaksi berhasil ditambahkan!")
        print()

        global stok_ayam
        global ayam_terjual  # Tambahkan jumlah ayam terjual
        stok_ayam -= jumlah_barang
        ayam_terjual += jumlah_barang  # Tambahkan jumlah ayam terjual
    else:
        print("Tidak ada pesanan yang ditambahkan.")
        
def menampilkan_transaksi():
    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        data.index += 1  # Ubah indeks mulai dari 1
        print(data)
    else:
        print("Tidak ada data transaksi yang tersimpan.")

# Fungsi untuk melihat stok ayam
def lihat_stok_ayam():
    print(f"Stok Ayam Geprek: {stok_ayam} ayam")
    print(f"Ayam Terjual Sementara: {ayam_terjual} ayam")

# Fungsi untuk mencetak laporan keuangan
def laporan_keuangan(namaFile):
    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        if not data.empty:
            # Menghitung total menu terjual tanpa menggunakan sum
            total_menu_terjual = data['Nama Barang'].str.contains("Ayam|Es").sum()

            print("===== Laporan Keuangan =====")
            print(f"Total Menu Terjual: {total_menu_terjual}")
            print(f"Total Ayam Tersisa: {stok_ayam} ayam")
            print(f"Total Pendapatan: RP. {total_menu_terjual * (harga_ayam_geprek + harga_ayam_bakar + harga_es_teh + harga_es_jeruk)}")
            print("==========================")
        else:
            print("Tidak ada data transaksi yang tersimpan.")
    else:
        print("Tidak ada data transaksi yang tersimpan.")
        

def hapus_transaksi():

    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        data.index += 1  # Ubah indeks mulai dari 1

        if not data.empty:
            print("Daftar Transaksi:")
            print(data)

            nomor_transaksi = int(input("Masukkan nomor transaksi yang ingin dihapus:"))

            if 1 <= nomor_transaksi <= len(data):
                data = data.drop(nomor_transaksi)
                data.reset_index(drop=True, inplace=True)
                data.to_csv(namaFile, index=False)
                print("Transaksi telah dihapus.")
            else:
                print("Nomor transaksi tidak valid.")
        else:
            print("Tidak ada data transaksi yang tersimpan.")
# Fungsi utama

def main():
    global stok_ayam
    stok_ayam = int(input("Masukkan stok awal Ayam Geprek: "))
    
    if not os.path.exists(namaFile):
        header = ['Tanggal', 'Nama Barang', 'Harga per Barang']
        pd.DataFrame(columns=header).to_csv(namaFile, index=False)

    while True:
        print("--------- Menu Kasir Ayam Geprek ---------")
        print("1. Tambahkan Transaksi")
        print("2. Menampilkan Transaksi")
        print("3. Lihat Stok Ayam Geprek")
        print("4. Laporan Keuangan")
        print("5. Hapus Transaksi")
        print("6. Keluar")
        pilihan = input("Pilih menu (1/2/3/4/5/6):")

        if pilihan == '1':
            tambahkan_transaksi()
        elif pilihan == '2':
            menampilkan_transaksi()
        elif pilihan == '3':
            lihat_stok_ayam()
        elif pilihan == '4':
            laporan_keuangan(namaFile)
        elif pilihan == '5':
            hapus_transaksi()  # Panggil fungsi hapus_transaksi
        elif pilihan == '6':
            break
        else:
            print("Pilihan tidak valid, silakan pilih angka 1 sampai 6")

if __name__ == "__main__":
    main()
