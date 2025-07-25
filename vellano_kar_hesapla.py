# Python script to calculate net profit for VELLANO bag sales based on user input


def vellano_kar_hesapla(
    satis_fiyati_usd,
    urun_maliyeti_usd,
    kargo_ucreti_usd,
    reklam_cpa_usd,
    odeme_komisyonu_oran,
    aylik_satis_adedi,
):
    """Satış başına ve aylık net kârı hesapla ve yazdır."""
    toplam_gider = (
        urun_maliyeti_usd
        + kargo_ucreti_usd
        + reklam_cpa_usd
        + (satis_fiyati_usd * odeme_komisyonu_oran)
    )
    net_kar = satis_fiyati_usd - toplam_gider
    aylik_net_kar = net_kar * aylik_satis_adedi

    print(f"Ürün başı net kâr: ${net_kar:.2f}")
    print(f"Aylık {aylik_satis_adedi} satış ile toplam net kâr: ${aylik_net_kar:.2f}")


if __name__ == "__main__":
    try:
        satis_fiyati_usd = float(input("Satış fiyatı (USD): "))
        urun_maliyeti_usd = float(input("Ürün maliyeti (USD): "))
        kargo_ucreti_usd = float(input("Kargo ücreti (USD): "))
        reklam_cpa_usd = float(input("Reklam CPA (USD): "))
        odeme_komisyonu_oran = float(input("Ödeme komisyon oranı (ör. 0.035): "))
        aylik_satis_adedi = int(input("Aylık satış adedi: "))
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    else:
        vellano_kar_hesapla(
            satis_fiyati_usd,
            urun_maliyeti_usd,
            kargo_ucreti_usd,
            reklam_cpa_usd,
            odeme_komisyonu_oran,
            aylik_satis_adedi,
        )
