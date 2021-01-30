import spidev
import time
import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', passwd = '1234'
                       , db='raspi_db')
curs = conn.cursor()
sql ="""insert into gasvalue(value) values(%s)"""


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def read_spi_adc(adcChannel):
	adcValue = 0
	buff = spi.xfer2([1,(8+adcChannel)<<4,0])
	adcValue=((buff[1]&3)<<8) + buff[2]
	return adcValue

def gas():
	try:
		while True:
			adcChannel = 0
			adcValue=read_spi_adc(adcChannel)
			print("gas %d"%adcValue)
			curs.execute(sql,(adcValue))
                	rs=curs.fetchall()
                	conn.commit()
			time.sleep(15)
	except KeyboardInterrupt:
		spi.close()
	finally:
	        conn.close()

