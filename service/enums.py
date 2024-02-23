class Algorithm:

    LEV = 'Расстояние Левенштейна'
    HAM = 'Расстояние Хэмминга'
    JAR = 'Расстояние Джаро'
    JW = 'Расстояние Джаро-Винклера'
    SH = 'Алгоритм шинглов'

    LEV_ALGS = LEV, HAM, JAR, JW

    CHOICES = (
        (LEV, LEV),
        (HAM, HAM),
        (JAR, JAR),
        (JW, JW),
        (SH, SH)
    )

    VALUES = (LEV, HAM, JAR, JW, SH)