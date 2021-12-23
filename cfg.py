#A - Старорусский
#B - Матричный
#C - Алгебраический
#D - Булева Алгебра
#E - IP - калькулятор
#F - Комплексные числа

app_names = dict(A='Калькулятор старорусских величин', B='Матричный калькулятор', C='Алгебраический калькулятор',
                 D='Калькулятор булевой алгебры', E='IP - калькулятор', F='Калькулятор комплексных чисел')

app_files = dict(A='oldr.exe', B='matrix.exe', C='documentC.exe',
                 D='Boolean_Calculate_Maven.jar', E='ip_calc.exe', F='complex.exe')

launch_args = dict(A='username localhost 2414 2417 businessapp 123456',
                   B='businessapp localhost 2414 2417 username 12345678',
                   C='businessapp localhost 2414 2417 username 12345678',
                   D='',
                   E='businessapp localhost 2414 2417 username 12345678',
                   F='')

address_to_server = ('localhost', 2414)

MYSQL_IP = 'localhost'
MYSQL_PORT = "2417"
DATABASE = 'MainCALCDB'
MYSQL_USER = 'root'
MYSQL_PASS = '123456'