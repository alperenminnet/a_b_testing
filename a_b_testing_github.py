import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats
# Gerekli importları yaptık.

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel(r"C:\Users\ALPEREN MİNNET\Desktop\DSMLBC\datasets\ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel(r"C:\Users\ALPEREN MİNNET\Desktop\DSMLBC\datasets\ab_testing.xlsx", sheet_name="Test Group")
#Kontrol ve test gruplarını okuttuk.

df_control = df_control[["Impression", "Click", "Purchase", "Earning"]]
df_test = df_test[["Impression", "Click", "Purchase", "Earning"]]
# Veri setinde bozukluklar olduğu için düzenlemeler yaptık. Sadece ilgilendiğimiz değişkenleri çektik.

# Hipotez kurulumu

# H0 : Maksimum bidding ile average biddingin dönüşü arasında istatistiksel olarak anlamlı bir fark yoktur.
# H1 : Maksimum bidding ile average biddingin dönüşü arasında istatistiksel olarak anlamlı bir fark vardır.

# Varsayım kontrolü yapmalıyız.


# Normallik varsayımı
# H0: Normallik varsayımı sağlanmaktadır.
# H1: sağlanmamaktadır.
test_stat, pvalue = shapiro(df_control["Purchase"]) #shapiro testi ile p_value değerine bakarak hipoteze karar veriyoruz.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p_value = 0.5891

test_stat, pvalue = shapiro(df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p_value = 0.1541

# p_value değeri 0.05'ten büyük olduğu için H0 reddedilemez.Normallik varsayımı sağlanır.

#Varyans homojenliği

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir


test_stat, pvalue = levene(df_control["Purchase"],
                           df_test["Purchase"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p_value = 0.1083
# p_value değeri 0.05'ten büyük olduğu için H0 reddedilemez. Varyanslar homejendir.

# Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) uygulanır.


test_stat, pvalue = ttest_ind(df_control["Purchase"],
                              df_test["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p_value = 0.3493

# p_value değeri 0.05'ten büyük olduğu için H0 reddedilemez. Bu yüzden diyebiliriz ki maksimum bidding ile average
# bidding arasında istatistiksel olarak bir fark yoktur.

df_control.head()
df_test.head()

df_control["Purchase"].mean() # 550.8940587702316
df_control["Earning"].mean() # 1908.568299802749

df_test["Purchase"].mean() # 582.1060966484677
df_test["Earning"].mean()# 2514.8907326506173


df_control["click_ad"] = df_control["Click"] / df_control["Impression"]
df_control["Impression"].mean() # 101711.44906769728 Ortalama görüntülenen reklam sayısı
df_control["click_ad"].mean() # 0.05361823086521902 Ortalama reklama tıklama sayısı
df_control["Click"].mean() / df_control["Impression"].mean() # 0.05014831092596444 Tıklamanın reklama oranı

df_test["click_ad"] = df_test["Click"] / df_test["Impression"]
df_test["Impression"].mean() # 120512.41175753452 Ortalama verilen reklam sayısı
df_test["click_ad"].mean() # 0.03417599154362738 Ortalama reklama tıklama sayısı
df_test["Click"].mean() / df_test["Impression"].mean() # 0.032922333085396625 Tıklamanın reklama oranı

# Ne kadar istatistiksel olarak anlam bulunmasa bile
# buradan görüldüğü üzere test grubunun satın alma ve kazanç oranları daha fazla
# Bu yüzden belirli bir süre yeni sistemde devam edebilirler. Belirli süre sonunda tekrar A/B testi
# yapıp durumu değerlendirebiliriz.
# Ayrıca görüldğü üzere test ekibinde daha fazla reklam gösterilmiş ve daha fazla kazanç sağlanmış. Eğer verdiğimiz reklam ücreti
# kazancımızdan fazla değilse burdan da sonuç olarak yeni sisteme devam etmemiz çıkabilir. Ama reklama tıklama oranı düşmüş
# onu da dikkate almamız gerekebilir.