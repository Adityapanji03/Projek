import os
import csv
import pandas as pd
from datetime import datetime

namaFile = "transaksi_kasir_ayam_geprek.csv"
menu_pesanan = "menu_geprek.csv"
stok_ayam = 0
ayam_terjual = 0

nama_pelanggan = ""
tipe_pesanan = ""
tanggal = ""
nama_barang = ""
total_harga = 0
pembayaran = ""

data_yang_dihapus = []
menu_kosong = []

import pandas as pd
import csv
from datetime import datetime

def tambahkan_transaksi():
    global nama_pelanggan, tipe_pesanan, tanggal, nama_barang, total_harga, pembayaran

    # Menggunakan tanggal saat ini
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nama_pelanggan = input("Masukkan nama pelanggan : ")
    
    menu_data = pd.read_csv(menu_pesanan)  # Baca data dari file CSV

    print("Pilih tipe pesanan:")
    print("1. Offline")
    print("2. Gofood")
    print("3. Shopeefood")
    print("4. Grab")
    print("5. Maxim")
    print("6. Online")
    print()
    input_tipe_pesanan = input('Masukkan Tipe pesanan: ')
    if  input_tipe_pesanan == '1':
        print("pesanan Offline.")
        tipe_pesanan = "Offline"
    elif input_tipe_pesanan == '2':
        print("pesanan Gofood.")
        tipe_pesanan = "Gofood"
    elif input_tipe_pesanan == '3':
        print("pesanan Shopeefood.")
        tipe_pesanan = "Shopeefood"
    elif input_tipe_pesanan == '4':
        print("pesanan Grab.")
        tipe_pesanan = "Grab"
    elif input_tipe_pesanan == '5':
        print("pesanan Maxim.")
        tipe_pesanan = "Maxim"
    elif input_tipe_pesanan == '6':
        print("pesanan Online.")
        tipe_pesanan = "Online"
    else:
        print("Tipe pesanan tidak valid. Silakan pilih angka dari 1 hingga 6.")

    pesanan = []
    while True:
      if os.path.exists(menu_pesanan):
        data = pd.read_csv(menu_pesanan)
        data.index += 1  # Ubah indeks mulai dari 1

        if not data.empty:
            print("===Daftar Menu===")
            print(data)

            nomor_transaksi = int(input("Masukkan nomor menu yang dipesan:"))

            if 1 <= nomor_transaksi <= len(data):
                # Ambil pesanan yang akan dihapus
                menu_pesan = data.loc[nomor_transaksi]

                # Tambahkan pesanan yang dihapus ke dalam list data_yang_dihapus
                menu_kosong.append(menu_pesan)

    if pesanan:
        nama_barang = ', '.join(pesanan)
        jumlah_barang = len(pesanan)

        # Hitung total harga pesanan
        total_harga = sum(menu_data.loc[menu_data['Nama'] == menu, 'Harga'].values[0] for menu in pesanan)

        print()
        print("Pilih pembayaran:")
        print("1. Tunai")
        print("2. Qris")
        print()
        input_pembayaran = input("Masukkan pilihan pembayaran:")
        if  input_pembayaran == '1':
            print("pesanan Tunai.")
            pembayaran = "Tunai"
        elif input_pembayaran == '2':
            print("pembayaran Qris.")
            pembayaran = "Qris"
        else:
            print("Input pembayaran tidak valid. Silakan pilih angka dari 1 hingga 2.")

        
def menampilkan_transaksi():
    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        data.index += 1  # Ubah indeks mulai dari 1
        print(data)
    else:
        print("Tidak ada data transaksi yang tersimpan.")

def menampilkan_menu():
    if os.path.exists(menu_pesanan):
        data = pd.read_csv(menu_pesanan)
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
        

histori_file = "pesanan_dihapus.csv"  # Definisikan variabel di luar fungsi

def hapus_transaksi():
    global data_yang_dihapus  # Tandai variabel sebagai global agar bisa diakses dan diubah di dalam fungsi

    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        data.index += 1  # Ubah indeks mulai dari 1

        if not data.empty:
            print("Daftar Transaksi:")
            print(data)

            nomor_transaksi = int(input("Masukkan nomor transaksi yang ingin dihapus:"))

            if 1 <= nomor_transaksi <= len(data):
                # Ambil pesanan yang akan dihapus
                pesanan_dihapus = data.loc[nomor_transaksi]

                # Tambahkan pesanan yang dihapus ke dalam list data_yang_dihapus
                data_yang_dihapus.append(pesanan_dihapus)

                # Hapus pesanan dari file asli
                data = data.drop(nomor_transaksi)
                data.reset_index(drop=True, inplace=True)
                data.to_csv(namaFile, index=False)
                print("Transaksi telah dihapus.")
            else:
                print("Nomor transaksi tidak valid.")
        else:
            print("Tidak ada data transaksi yang tersimpan.")
        
        pilihan = input("Ingin melihat histori pembatalan pesanan? (ya/tidak): ")
        if pilihan == 'ya' and data_yang_dihapus:
            # Simpan data yang dihapus dalam file CSV baru ("pesanan_dihapus.csv")
            histori_file = "pesanan_dihapus.csv"
            histori = pd.DataFrame(data_yang_dihapus)
            if not os.path.exists(histori_file):
                header = ['Nama', 'Tipe Pesanan', 'Tanggal', 'Nama Barang', 'Total Harga', 'Pembayaran']
                histori.to_csv(histori_file, index=False)
            else:
                histori.to_csv(histori_file, mode='a', header=False, index=False)

            # Tampilkan data yang dihapus dalam sebuah DataFrame
            data_histori = pd.read_csv(histori_file)
            data_histori.index += 1  # Ubah indeks mulai dari 1
            print("Histori Pembatalan Pesanan:")
            print(data_histori)
        elif pilihan == 'ya':
            print("Tidak ada histori pembatalan pesanan.")

def cetak_struk(namaFile):
    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        data.index += 1  # ngubah indeks mulai dari 1

        if not data.empty:
            print("Daftar Transaksi:")
            print(data)

        input_struk = input("Masukkan baris yang ingin dicetak dalam struk :")

def member_geprek():
    while True:
        print("=====Menu Member Geprek=====")
        print("1. Daftar Member")
        print("2. Cek Member")
        print("3. Pembaharuan")
        print()
        input_member = input("Masukkan nomor menu yang diinginkan: ")

        if input_member == '1':
            print()
            print("Menu Pendaftaran member")
        elif input_member == '2':
            print()
            print("Menu Cek member")
        elif input_member == '3':
            print()
            print("Menu Pembaharuan member")
        else:
            print("Tipe pesanan tidak valid. Silakan pilih angka dari 1 hingga 3.")

def cek_histori():
    pilihan = input("Ingin melihat histori pembatalan pesanan? (Tekan enter untuk melihat histori): ")
    
    if pilihan == '' and data_yang_dihapus:
        histori_file = "pesanan_dihapus.csv"
        histori = pd.DataFrame(data_yang_dihapus)
        
        if not os.path.exists(histori_file):
            header = ['Nama', 'Tipe Pesanan', 'Tanggal', 'Nama Barang', 'Total Harga', 'Pembayaran']
            histori.to_csv(histori_file, index=False, header=header)
        else:
            histori.to_csv(histori_file, mode='a', header=False, index=False)

        data_histori = pd.read_csv(histori_file)
        data_histori.index += 1  # Ubah indeks mulai dari 1
        print("Histori Pembatalan Pesanan:")
        print(data_histori)
        
    elif pilihan == '':
        print("Tidak ada histori pembatalan pesanan.")


# Fungsi utama
def main():
    global stok_ayam
    stok_ayam = int(input("Masukkan stok awal Ayam Geprek: "))
    data_menu = {
        'Nama Menu': [],
        'Harga': []
    }

    while True:
        nama_menu = input("Masukkan nama menu (enter untuk selesai): ")
        if not nama_menu:
            break

        try:
            harga_menu = int(input(f"Masukkan harga menu {nama_menu}: "))
            data_menu['Nama Menu'].append(nama_menu)
            data_menu['Harga'].append(harga_menu)
            print(f"Menu {nama_menu} dengan harga Rp {harga_menu} berhasil ditambahkan.")
        except ValueError:
            print("Masukkan harga dalam bentuk angka.")

    menu_df = pd.DataFrame(data_menu)

    # Menyimpan menu ke file CSV
    menu_df.to_csv(menu_pesanan, index=False)
    print("Data menu telah disimpan ke 'menu_geprek.csv'.")
    
    if not os.path.exists(namaFile):
        header = ['Nama', 'Tipe Pesanan','Tanggal', 'Nama Barang', 'Total Harga', 'Pembayaran']
        pd.DataFrame(columns=header).to_csv(namaFile, index=False)

    while True:
        print("--------- Menu Kasir Ayam Geprek ---------")
        print("1. Tambahkan Transaksi")
        print("2. Menampilkan Transaksi")
        print("3. Lihat Stok Ayam Geprek")
        print("4. Laporan Keuangan")
        print("5. Hapus Transaksi")
        print("6. Cek Histori")
        print("7. Cetak Struk")
        print("8. Pendaftaran dan Pengecekan Member")
        print("9. Tampilkan menu")
        print("10. Keluar")
        pilihan = input("Pilih menu (1/2/3/4/5/6/7/8/9/10):")

        if pilihan == '1':
            tambahkan_transaksi()
        elif pilihan == '2':
            menampilkan_transaksi()
        elif pilihan == '3':
            lihat_stok_ayam()
        elif pilihan == '4':
            laporan_keuangan(namaFile)
        elif pilihan == '5':
            hapus_transaksi()
        elif pilihan == '6':
            cek_histori()
        elif pilihan == '7':
            cetak_struk(namaFile)
        elif pilihan == '8':
            member_geprek()
        elif pilihan == '9':
            menampilkan_menu()
        elif pilihan == '10':
            break
        else:
            print("Pilihan tidak valid, silakan pilih angka 1 sampai 10")

if __name__ == "__main__":
    main()
