
#==========================
# ===== Extract File ======
#==========================

from ReadRawData import *
#from ReadHyperRawData import *

import time

start_time = time.time()

FilePath = "E:\\2016-2017\\05-Feb-2017\\3D\Dataset-3D\\23-Feb-2017-3D"

PathPNGFlir = ''

PathPNGVis = ''


ReadRawData(FilePath, 'weather', 'weather_position', '')

ReadRawData(FilePath, 'par', 'par_position', '')

ReadRawData(FilePath, 'temp', 'temp_position', '')

ReadRawData(FilePath, 'relh', 'relh_position', '')

ReadRawData(FilePath, 'vis', 'vis_position', PathPNGVis)

# ReadRawData(FilePath, 'flir', 'flir_position', PathPNGFlir)

# ReadRawData(FilePath, '3d', '3d_position', '')

# ReadRawData(FilePath, 'ps2', 'ps2_position', '')

# ReadRawData(FilePath, 'ndvi', 'ndvi_position', '')

# ReadHyperRawData(FilePath, 'vnir', 'vnir_position', 'Dataset-vnir')


print("--- %s seconds ---" % (time.time() - start_time))