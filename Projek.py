import os
import csv
import pandas as pd
from datetime import datetime
import time
import random
from tabulate import tabulate

namaFile = "transaxksi_kasir_ayam_geprek.csv"
menu_file = "menu_geprek.csv"
member_csv = 'member_data.csv'

ayam_terjual = 0
nama_pelanggan = ""
tipe_pesanan = ""
tanggal = ""
nama_barang = ""
total_harga = 0
pembayaran = ""
username = ""

data_yang_dihapus = []
menu_kosong = []

def cetak_struk(namaFile):
    os.system("cls")
    try:
        transaksi_data = pd.read_csv(namaFile)
        if not transaksi_data.empty:
            latest_transaksi = transaksi_data.iloc[-1]
            
            # Meminta input uang pembeli
            uang_pembeli = float(input("Masukkan jumlah uang pembeli: Rp "))
            os.system('cls')
            # Menghitung kembalian
            kembalian = uang_pembeli - latest_transaksi['Total Harga']

            # Menampilkan struk
            print("\n=== Struk Pembelian ===")
            print(f"Tanggal       : {latest_transaksi['Tanggal']}")
            print(f"Nama Pelanggan: {latest_transaksi['Nama']}")
            print(f"Tipe Pesanan  : {latest_transaksi['Tipe Pesanan']}")
            print(f"Nama Barang   : {latest_transaksi['Nama Barang']}")
            print(f"Total Harga   : Rp {latest_transaksi['Total Harga']}")

            # Menampilkan diskon member jika member
            if 'Diskon Member' in latest_transaksi and latest_transaksi['Diskon Member'] > 0:
                print(f"Diskon Member : {latest_transaksi['Diskon Member'] * 100}%")

            print(f"Uang Pembeli  : Rp {uang_pembeli}")
            print(f"Kembalian     : Rp {kembalian}")
            print(f"Pembayaran    : {latest_transaksi['Pembayaran']}")
            print(f"Nama Kasir    : {latest_transaksi['Nama Kasir']}")
            print("======================\n")
        else:
            print("Data transaksi masih kosong. Silakan tambahkan transaksi terlebih dahulu.\n")
    except pd.errors.EmptyDataError:
        print("Data transaksi masih kosong. Silakan tambahkan transaksi terlebih dahulu.\n")

        
def load_menu_data():
    if os.path.exists(menu_file):
        data_menu = pd.read_csv(menu_file)
        data_menu.index += 1
    else:
        data_menu = pd.DataFrame(columns=['Nama Menu', 'Harga'])

    return data_menu

def display_menu(data_menu):
    if not data_menu.empty:
        # Use tabulate to display the menu in a tabular format
        data_menu.index += 1
        print(tabulate(data_menu, headers='keys', tablefmt='grid'))
    else:
        print("Menu kosong. Silakan tambahkan menu terlebih dahulu.")

def tambahkan_transaksi():
    os.system("cls")
    global nama_pelanggan, tipe_pesanan, tanggal, nama_barang, total_harga_pesanan, pembayaran, username

    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nama_pelanggan = input("Masukkan nama pelanggan: ")

    while True:
        os.system('cls')
        print("Pilih tipe pesanan:")
        print("1. Offline")
        print("2. Gofood")
        print("3. Shopeefood")
        print("4. Grab")
        print("5. Maxim")
        print("6. Online")
        print()
        input_tipe_pesanan = input('Masukkan Tipe pesanan: ')

        if input_tipe_pesanan in ['1', '2', '3', '4', '5', '6']:
            break
        else:
            print("Tipe pesanan tidak valid. Silakan pilih angka dari 1 hingga 6.")

    if input_tipe_pesanan == '1':
        print("Pesanan Offline.")
        tipe_pesanan = "Offline"
    elif input_tipe_pesanan == '2':
        print("Pesanan Gofood.")
        tipe_pesanan = "Gofood"
    elif input_tipe_pesanan == '3':
        print("Pesanan Shopeefood.")
        tipe_pesanan = "Shopeefood"
    elif input_tipe_pesanan == '4':
        print("Pesanan Grab.")
        tipe_pesanan = "Grab"
    elif input_tipe_pesanan == '5':
        print("Pesanan Maxim.")
        tipe_pesanan = "Maxim"
    elif input_tipe_pesanan == '6':
        print("Pesanan Online.")
        tipe_pesanan = "Online"

    os.system('cls')
    data_menu = pd.read_csv(menu_file)
    display_menu(data_menu)
        
    pesanan = []
    total_harga_pesanan = 0
    diskon = 0.0

    # Display menu

    
    while True:
        nomor_transaksi = input("Masukkan nomor menu yang dipesan (enter untuk selesai): ")

        if not nomor_transaksi:
            break

        try:
            nomor_transaksi = int(nomor_transaksi)
            if 1 <= nomor_transaksi <= len(data_menu):
                menu_pesan = data_menu.loc[nomor_transaksi]  # Adjust index
                pesanan.append(menu_pesan['Nama Menu'])
                if nama_barang:  # Check if nama_barang is not empty
                    nama_barang += ", "
                nama_barang += menu_pesan['Nama Menu']  # Update nilai nama_barang

                harga_menu = menu_pesan['Harga']
                total_harga_pesanan += harga_menu
                print(f"Menu {menu_pesan['Nama Menu']} dengan harga Rp {harga_menu} ditambahkan ke pesanan.")
            else:
                print("Nomor menu tidak valid. Silakan pilih nomor yang sesuai.")
        except ValueError:
            print("Masukkan nomor menu dalam bentuk angka.")

    while True:
        os.system('cls')
        print()
        print("Pilih pembayaran:")
        print("1. Tunai")
        print("2. Qris")
        print()
        input_pembayaran = input("Masukkan pilihan pembayaran:")
        if input_pembayaran == '1':
            print("Pembayaran Tunai.")
            pembayaran = "Tunai"
            break
        elif input_pembayaran == '2':
            print("Pembayaran Qris.")
            pembayaran = "Qris"
            break
        else:
            print("Input pembayaran tidak valid. Silakan pilih angka dari 1 hingga 2.")
    
    os.system("cls")
    print("Ringkasan Pesanan : ")
    print(f"Nama {nama_pelanggan}, Tipe Pesanan {tipe_pesanan}, Nama Menu {nama_barang}, Pembayaran {pembayaran}")

    while True:
        print()
        print("Apakah pesanan sudah benar?:")
        print("1. Ya")
        print("2. Kembali ke menu menambah transaksi")
        print()
        lanjut = input("Masukkan pilihan:")
        if lanjut == '1':
            break
        elif lanjut == '2':
            tambahkan_transaksi()

    while True:
        os.system('cls')
        member_input = input("Apakah pelanggan adalah member? (ya/tidak): ").lower()

        while member_input not in ['ya', 'tidak']:
             print("Input tidak valid. Silakan masukkan 'ya' atau 'tidak'.")
        
        member_tidak = member_input == 'tidak'
        if member_tidak:
            break

        member = member_input == 'ya'

        if member:
            #while True:
            kode_member = input("Masukkan Kode Member (Enter untuk melanjutkan): ")
            member_info = pd.read_csv(member_csv)

            if member_info['ID'].eq(kode_member).any():
                print("Member ditemukan. Anda mendapatkan diskon 10%.")
                diskon = 0.1
                break
            elif kode_member == '':
                break
            else:
                print("Kode Member tidak valid. Silakan coba lagi.")
        else:
            diskon = 0.0

    total_harga_pesanan *= (1 - diskon)

    transaksi = pd.DataFrame({
        'Nama': [nama_pelanggan],
        'Tipe Pesanan': [tipe_pesanan],
        'Tanggal': [tanggal],
        'Nama Barang': [nama_barang],
        'Total Harga': [total_harga_pesanan],
        'Pembayaran': [pembayaran],
        'Nama Kasir': [username]
    }, columns=['Nama', 'Tipe Pesanan', 'Tanggal', 'Nama Barang', 'Total Harga', 'Pembayaran', 'Nama Kasir'])

    if not os.path.exists(namaFile):
        header = ['Nama', 'Tipe Pesanan', 'Tanggal', 'Nama Barang', 'Total Harga', 'Pembayaran', "Nama Kasir"]
        transaksi.to_csv(namaFile, index=False, header=header)
    else:
        transaksi.to_csv(namaFile, mode='a', header=False, index=False)

    os.system('cls')
    pilihan = input("Ingin mencetak struk? (ya/tidak)")
    if pilihan == "ya":
        cetak_struk(namaFile)
    elif pilihan == "tidak":
        print("Struk tidak dicetak")

    print()
    print("Transaksi berhasil ditambahkan!")
    print()

def cek_menu():
  os.system("cls")
  data_menu = load_menu_data()

  
  print("===Daftar Menu===")
  print(data_menu)

def cari_transaksi_berdasarkan_nama():
    if os.path.exists(namaFile):
        try:
            data = pd.read_csv(namaFile)
            data.index += 1  # Ubah indeks mulai dari 1

            nama_pembeli_cari = str(input("Masukkan nama pembeli yang ingin dicari: ")).strip()

            # Filter data berdasarkan nama pembeli
            hasil_pencarian = data[data['Nama'].str.contains(nama_pembeli_cari, case=False, na=False)]

            if not hasil_pencarian.empty:
                print(f"Hasil pencarian untuk nama pembeli '{nama_pembeli_cari}':")
                print(hasil_pencarian)
            else:
                print(f"Tidak ditemukan transaksi untuk nama pembeli '{nama_pembeli_cari}'.")
        except pd.errors.EmptyDataError:
            print("Data transaksi masih kosong. Silakan tambahkan transaksi terlebih dahulu.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Tidak ada data transaksi yang tersimpan.")


def menampilkan_transaksi():
    os.system('cls')
    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        data.index += 1
        print(data)
    else:
        print("Tidak ada data transaksi yang tersimpan.")
       
    print()
    cari = input("ingin mencari data transaksi? (y/n):")
    os.system('cls')
    if cari == 'y':
        os.system('cls')
        cari_transaksi_berdasarkan_nama()
     

# Fungsi untuk mencetak laporan keuangan
def laporan_keuangan(namaFile):
    os.system("cls")
    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        if not data.empty:
            # Menghitung total pendapatan berdasarkan kolom Total Harga
            total_pendapatan = data['Total Harga'].sum()

            # Menghitung jumlah pesanan
            jumlah_pesanan = data.shape[0]
            print("===== Laporan Keuangan =====")
            print(f"Total Pendapatan: Rp {total_pendapatan}")
            print(f"Jumlah Pesanan: {jumlah_pesanan}")
            print("==========================")
        else:
            print("Tidak ada data transaksi yang tersimpan.")
    else:
        print("Tidak ada data transaksi yang tersimpan.")
       
os.system('cls')
histori_file = "pesanan_dihapus.csv"  # Definisikan variabel di luar fungsi

def hapus_transaksi():
    os.system("cls")
    global data_yang_dihapus  # Tandai variabel sebagai global agar bisa diakses dan diubah di dalam fungsi

    if os.path.exists(namaFile):
        data = pd.read_csv(namaFile)
        data.index += 1  # Ubah indeks mulai dari 1

        if not data.empty:
            print("Daftar Transaksi:")
            print(data)

            nomor_transaksi = input("Masukkan nomor transaksi yang ingin dihapus (Enter untuk melihat histori pesanan yang dihapus):")

            if nomor_transaksi == '':
                print()
                print("Anda tidak menghapus data transaksi")
            else:
                try:
                    nomor_transaksi = int(nomor_transaksi)

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
                except ValueError:
                    print("Masukkan nomor transaksi dalam bentuk angka.")
        else:
            print("Tidak ada data transaksi yang tersimpan.")
        
        pilihan = input("Ingin melihat histori pembatalan pesanan? (ya/tidak): ")
        if pilihan == 'ya' and data_yang_dihapus:
            # Simpan data yang dihapus dalam file CSV baru ("pesanan_dihapus.csv")
            histori_file = "pesanan_dihapus.csv"
            histori = pd.DataFrame(data_yang_dihapus)
            if not os.path.exists(histori_file):
                header = ['Nama', 'Tipe Pesanan', 'Tanggal', 'Nama Barang', 'Total Harga', 'Pembayaran', 'Nama Kasir']
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

def generate_member_id(nama, id_member):
    while True:
        inisial = ''.join(word[0] for word in nama.upper().split())
        kode_unik = inisial + str(random.randint(100, 999))
        if kode_unik not in id_member:
            return kode_unik

def register_member():
    os.system('cls')
    try:
        member_df = pd.read_csv(member_csv)
    except FileNotFoundError:
        member_df = pd.DataFrame(columns=['Nama', 'ID', 'Jenis Kelamin', 'Umur', 'Pekerjaan', 'Alamat'])

    while True:
        print("Menu Pendaftaran Member")
        nama_member = input("Masukkan nama member: ")

        if member_df['Nama'].str.lower().eq(nama_member.lower()).any():
            print("Nama sudah terdaftar. Silakan masukkan nama lain.")
        else:
            break
    while True:
      os.system('cls')
      id_member = set(member_df['ID'])
      new_member_id = generate_member_id(nama_member, id_member)

      jenis_kelamin = input("Masukkan jenis kelamin (L/P): ")
      umur = input("Masukkan umur: ")
      pekerjaan = input("Masukkan pekerjaan: ")
      alamat = input("Masukkan alamat: ")
      
      print(f"Nama {nama_member}, Gender {jenis_kelamin}, Umur {umur}, Pekerjaan {pekerjaan}, Alamat {alamat}")
      print("Apakah informasi member sudah  benar?")
      print()
      print("1. Ya")
      print("2. Kembali ke menu daftar member")
      print()
      lanjut = input("Masukkan pilihan:")
      if lanjut == '1':
        break
      elif lanjut == '2':
        register_member()
    
    

    new_member_df = pd.DataFrame({
        'Nama': [nama_member],
        'ID': [new_member_id],
        'Jenis Kelamin': [jenis_kelamin],
        'Umur': [umur],
        'Pekerjaan': [pekerjaan],
        'Alamat': [alamat]
    })

    member_df = pd.concat([member_df, new_member_df], ignore_index=True)

    member_df.to_csv(member_csv, index=False)

    print(f"Registrasi berhasil! Member ID Anda adalah: {new_member_id}")
    print()

def check_member():
    print("Menu Cek Member")
    member_id = input("Masukkan ID member: ")

    try:
        member_df = pd.read_csv(member_csv)

        member_info = member_df[member_df['ID'] == member_id]

        if not member_info.empty:
            print("Informasi Member:")
            print(member_info)
        else:
            print("Member tidak ditemukan.")
    except FileNotFoundError:
        print("File CSV tidak ditemukan. Tidak ada member terdaftar.")

    print()

def member_geprek():
    os.system("cls")
    while True:
        print("=====Menu Member Geprek=====")
        print("1. Daftar Member")
        print("2. Cek Member")
        print("3. Keluar")
        print()
        input_member = input("Masukkan nomor menu yang diinginkan: ")
        os.system('cls')
        if input_member == '1':
            register_member()
        elif input_member == '2':
            check_member()
        elif input_member == '3':
            break
        else:
            print("Tipe pesanan tidak valid. Silakan pilih angka dari 1 hingga 3.")

def check_username():
    global username
    with open("login_database.csv", 'r', newline="") as file3:
        reader = csv.reader(file3)

        for line in reader:
            if username == line[0]:
                print("Username telah terdaftar, silahkan memilih menu login")
                return True
        return False
        
def login():
    global username
    while True:
        with open("login_database.csv", 'r', newline="") as file1:
            reader = csv.reader(file1)

            for line in reader:
                if username == line[0]:
                    password = input('Masukkan password akun anda : ')
                    if password == line[1]:
                        print('Log in berhasil. ')
                        return True
                    else:
                        print('Password salah. Silakan coba lagi.')
                        break
            else:
                print('Username ini tidak terdaftar. Silakan coba lagi atau daftar terlebih dahulu.')
        
        print()
        print("Coba Lagi...")
        print()
        main()
    

def register():
    global username
    username = input("Masukkan username yang ingin didaftarkan : ")

    if check_username():
        return

    file2 = open("login_database.csv", 'a', newline="")
    writer = csv.writer(file2)
    
    print('\n', 'Loading...', '\n')

    for seconds in range(5, 0, -1):
        time.sleep(1)
    print('======Username telah terdaftar======')

    while True:
        password = input("Buat password 8 kombinasi (harus mengandung satu angka, satu huruf kapital dan satu simbol) : ")
        if password == "":
            print('Password tidak boleh kosong')
        elif len(password) >= 8 and any(char.isdigit() for char in password) \
                and any(char.isupper() for char in password) and any(not char.isalnum() for char in password):
                    print('\n', f'====== Akun telah terdaftar. Selamat datang {username} ======', '\n')
                    writer.writerow([username, password])
                    file2.close()
                    break
        else:
            print("Password tidak aman")
    return False

def check_login_csv():
    login_csv = "login_database.csv"

    if not os.path.exists(login_csv):
        with open(login_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Menulis header ke file CSV jika file baru dibuat
            writer.writerow(["Username", "Password"])

# Fungsi utama
def main():
    os.system("cls")
    global username

    # Memanggil fungsi untuk memeriksa dan membuat file login jika belum ada
    check_login_csv()

    masuk = input('Apakah anda telah memiliki akun? (ya/tidak) : ')
    if masuk == 'ya':
        username = input('Masukkan username anda : ')
        login()
    else:
        register()

    os.system('cls')
    data_menu = load_menu_data()
    while True:
        nama_menu = input("Masukkan nama menu (enter untuk selesai): ")
        if not nama_menu:
            break

        try:
            harga_menu = int(input(f"Masukkan harga menu {nama_menu}: "))
            data_menu = data_menu._append({'Nama Menu': nama_menu, 'Harga': harga_menu}, ignore_index=True)
            print(f"Menu {nama_menu} dengan harga Rp {harga_menu} berhasil ditambahkan.")
        except ValueError:
            print("Masukkan harga dalam bentuk angka.")

    # Save menu data to the combined CSV file
    data_menu.to_csv(menu_file, index=False)
    print(f"Data menu telah disimpan ke '{menu_file}'.")

    if not os.path.exists(namaFile):
        header = ['Nama', 'Tipe Pesanan','Tanggal', 'Nama Barang', 'Total Harga', 'Pembayaran', 'Nama Kasir']
        pd.DataFrame(columns=header).to_csv(namaFile, index=False)
    os.system('cls')
    while True:
        print('\n', "--------- Menu Kasir Ayam Geprek ---------")
        print("1. Tambahkan Transaksi")
        print("2. Menampilkan Transaksi")
        print("3. Laporan Keuangan")
        print("4. Hapus Transaksi")
        print("5. Pendaftaran dan Pengecekan Member")
        print("6. Cek Menu")
        print("7. Login + Menambah menu baru")
        print("8. Keluar")
        pilihan = input("Pilih menu (1/2/3/4/5/6/7/8):")

        if pilihan == '1':
            tambahkan_transaksi()
        elif pilihan == '2':
            menampilkan_transaksi()
        elif pilihan == '3':
            laporan_keuangan(namaFile)
        elif pilihan == '4':
            hapus_transaksi()
        elif pilihan == '5':
            member_geprek()
        elif pilihan == '6':
            display_menu(data_menu)
        elif pilihan == '7':
            main()
        elif pilihan == '8':
            break
        else:
            print("Pilihan tidak valid, silakan pilih angka 1 sampai 7")

if __name__ == "__main__":
    main()
