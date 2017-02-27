import glob
import os
import zipfile
import untangle
import numpy as np
import shutil
import math
import skimage.io

import os.path

# from matplotlib import pylab as plt
import cv2

from readVisRaw import *

# import tifffile
from PIL import Image
from libtiff import TIFF
import skimage.io

def ReadRawData(filePath, filename, filepose, PngPath):

    try:
        for directories in os.listdir(filePath):
            subdirectories = os.path.join(filePath, directories)
            if os.path.isdir(subdirectories):

                # === read info.txt file / Extract plot ID tag
                textInfo = os.path.join(subdirectories, "info.txt")

                IDtag = open(textInfo).read().splitlines()
                ID = IDtag[0].split(':')
                plotID = ID[1].replace("\r\n","") #remove \n\r
                plotID = plotID.replace(" ", "")  #remove space

                path = os.path.join(subdirectories, filename)

                #== counter for PS2
                cnt = 0

                #===== Read .raw file inside the subfolder
                for infile in glob.glob( os.path.join(path, '*.rawx') ):
                    print("Reading Folder: " + path)

                    #==== Change the .rawx format to .zip format
                    pre, ext = os.path.splitext(infile)
                    os.rename(infile, pre + '.zip')

                    #==== unzip file
                    zipPath = pre + '.zip'
                    zfile = zipfile.ZipFile(zipPath)
                    zfile.extractall(path)
                    zfile.close()

                    Datadir = os.path.join(subdirectories, 'Dataset')
                    # === Create Dataset Folder if it doesn't exist
                    if not os.path.exists(Datadir):
                        os.makedirs(Datadir)
                    DatasetFolder = os.path.join(Datadir, filename)

                    # ===========================
                    # ==== Read RGB raw file ====
                    # ===========================
                    if filename == 'vis':
                        imageFile = os.path.join(path, "image.raw")

                        # ==== read raw vis image =====
                        #==============================
                        # ==== read xml file
                        infoFile = os.path.join(path, "info.xml")
                        obj = untangle.parse(infoFile)

                        RGBrows = int(obj.rawImage.width['value']) #3296
                        RGBcols = int(obj.rawImage.height['value']) #2472

                        #=== read vis raw file
                        img_rot = readVisRaw(imageFile, RGBcols, RGBrows)

                        """A = np.fromfile(imageFile, dtype='uint8', count=-1, sep="")
                        A = A.reshape([RGBcols, RGBrows])
                        #img = cv2.cvtColor(A, cv2.COLOR_BAYER_GR2BGR)
                        img = cv2.cvtColor(A, cv2.COLOR_BAYER_GR2RGB)

                        #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                        #cv2.imshow('image', img)

                        # === Rotate the image 90 degree ===
                        rangle = np.deg2rad(-90)  # angle in radians
                        h = RGBcols
                        w = RGBrows
                        # === now calculate new image width and height ===
                        nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * 1.0
                        nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * 1.0
                        # === ask OpenCV for the rotation matrix ===
                        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), -90, 1.0)
                        # === calculate the move from the old center to the new center combined with the rotation ===
                        rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
                        # === the move only affects the translation, so update the translation part of the transform ===
                        rot_mat[0, 2] += rot_move[0]
                        rot_mat[1, 2] += rot_move[1]
                        img_rot = cv2.warpAffine(img, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)"""


                        # === Save the RGB image in separate folder === #
                        # ============================================= #
                        """ImgDataFile = os.path.join(PngPath, plotID + ".png")
                           cv2.imwrite(ImgDataFile, img_rot)"""


                        '''cv2.namedWindow('image_rot', cv2.WINDOW_NORMAL)
                        cv2.imshow('image_rot', img_rot)
                        plt.imshow(img_rot)
                        plt.axis('off')
                        plt.show()
                        '''

                        #=== rename raw vis image and move it to Dataset folder
                        visImgRaw = os.path.join(path, "vis-raw" + "_" + plotID + ".raw")
                        os.rename(imageFile, visImgRaw)  # rename image.raw
                        shutil.move(visImgRaw, Datadir)  # move vis image.raw file to Dataset dir

                        visInfo = os.path.join(path, "vis-info" + "_" + plotID + ".xml")

                        os.rename(infoFile, visInfo)  # rename info.xml
                        shutil.move(visInfo, Datadir)  # move the info.xml file

                    # ==========================
                    # === Read FLIR raw file ===
                    # ==========================
                    elif filename == 'flir':
                        imageFile = os.path.join(path, "image.raw")

                        # ==== read raw flir image
                        #=========================

                        # ==== read xml file
                        infoFile = os.path.join(path, "info.xml")
                        obj = untangle.parse(infoFile)

                        FlirRow = int(obj.rawImage.height['value']) #480
                        FlirCol = int(obj.rawImage.width['value']) #640

                        img = np.fromfile(imageFile, dtype='uint16', count=-1, sep="")
                        img = img.reshape([FlirCol, FlirRow])

                        # === flip the image horizontally ===
                        img_flip = cv2.flip(img, 0)

                        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                        # cv2.imshow('image', img_flip)

                        #plt.imshow(img_rot)
                        #plt.axis('off')
                        #plt.show()

                        # === Save the FLIR image in separate folder === #
                        # ============================================= #
                        """ImgDataFile = os.path.join(PngPath, plotID + ".png")
                        cv2.imwrite(ImgDataFile, img_flip)"""

                        # === rename and save FLIR raw image in the Dataset folder ===
                        # === ========================================================
                        """ImgDataFile = os.path.join(PngPath, plotID + ".png")
                        cv2.imwrite(ImgDataFile, img_flip)"""

                        # rename raw flir image and move it to Dataset folder
                        flirImgRaw = os.path.join(path, "flir-raw" + "_" + plotID + ".raw")

                        os.rename(imageFile, flirImgRaw)  # rename image.raw
                        shutil.move(flirImgRaw, Datadir)  # move flir image.raw file to Dataset dir

                        flirInfo = os.path.join(path, "flir-info" + "_" + plotID + ".xml")

                        os.rename(infoFile, flirInfo)  # rename info.xml
                        shutil.move(flirInfo, Datadir)


                    # ==========================
                    # === Read PS2 raw file ===
                    # ==========================
                    elif filename == 'ps2':
                        imageFile = os.path.join(path, "image.raw")

                        # ==== read raw ps2 image
                        #=========================

                        # ==== read xml file
                        infoFile = os.path.join(path, "info.xml")
                        obj = untangle.parse(infoFile)

                        PS2Row = int(obj.rawImage.height['value']) #1038
                        PS2Col = int(obj.rawImage.width['value']) #1388

                        img = np.fromfile(imageFile, dtype='uint16', count=-1, sep="")

                        img = img.reshape([PS2Row, PS2Col])

                        if cnt == 0:
                            img_layer = np.zeros((img.shape[0], img.shape[1], 25), 'uint16')
                            fileNameAll = np.zeros((25,1))


                        # split the path of ps2 file
                        PS2FileName = os.path.split(pre)
                        ps2files = PS2FileName[1].split("_")

                        #=== store ps2 image in a multi layer image
                        img_layer[:,:,cnt] = img
                        #=== store ps2 file names in an array
                        fileNameAll[cnt] = int(ps2files[0])

                        cnt += 1

                        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                        # cv2.imshow('image', img)

                        #plt.imshow(img)
                        #plt.axis('off')
                        #plt.show()

                    # ========================
                    # === Read 3D raw file ===
                    # ========================
                    elif filename == '3d':
                        image3draw = os.path.join(path, "image.raw")

                        # ==== Change the .rawx format to .zip format ====
                        pre, ext = os.path.splitext(image3draw)
                        os.rename(image3draw, pre + '.zip')

                        # ==== unzip file ====
                        zipPath = pre + '.zip'
                        zfile = zipfile.ZipFile(zipPath)
                        zfile.extractall(path)
                        zfile.close()

                        # === move sensor.ply file to Dataset folder ====
                        sensor0 = os.path.join(path, "sensor0.ply")
                        sensor1 = os.path.join(path, "sensor1.ply")

                        sensor0Path = os.path.join(path, "sensor0" + "_" + plotID + ".ply")
                        os.rename(sensor0, sensor0Path)  # rename sensor0.ply
                        shutil.move(sensor0Path, Datadir)  # move sensor0 file to Dataset dir

                        sensor1Path = os.path.join(path, "sensor1" + "_" + plotID + ".ply")
                        os.rename(sensor1, sensor1Path)  # rename sensor1.ply
                        shutil.move(sensor1Path, Datadir)  # move sensor1 file to Dataset dir

                    # =========================================
                    # ==== Read Par,NDVI,RelH,Weather,Temp ====
                    # =========================================
                    else:
                        # ==== Change the image.raw to image.xml ====
                        imageFile = os.path.join(path, "image.raw")

                        preImg, extImg = os.path.splitext(imageFile)
                        os.rename(imageFile, preImg + '.xml')

                        FileXML = os.path.join(path, filename + "_" + plotID + ".xml")
                        imageXML = os.path.join(path, "image.xml")

                        os.rename(imageXML, FileXML) # rename image.xml to filename.xml
                        shutil.move(FileXML, Datadir) # move xml file to Dataset dir

                        '''
                        # ==== Read xml file ====
                        DataName = list()
                        tree = ET.parse(imageXML)
                        root = tree.getroot()
                        for subdirectoriesXML in root:
                            xmlValue = subdirectoriesXML.attrib.values()
                            DataName.append(float(xmlValue[0]))
                        #print DataName   #print the values inside the XML file

                        # ==== Save data to a file ====
                        info = np.asarray(DataName)
                        DatasetFileName = DatasetFolder + '_' + plotID
                        np.save(DatasetFileName,info)
                        '''


                #==== save PS2 values
                if filename == 'ps2':

                    #=== sort ps2 file name from 0 to 25
                    ps2NameIndx = np.argsort(fileNameAll, axis=0)


                    # rename raw flir image and move it to Dataset folder
                    ps2Img = os.path.join(Datadir, "ps2-Multiband" + "_" + plotID + ".tiff")

                    #=== write ps2 image as tif file
                    tiff = TIFF.open(ps2Img, 'w')
                    for jj in range(0,25):
                        tiff.write_image(img_layer[:,:, int(ps2NameIndx[jj])])
                    tiff.close()

                    #=== rename and more info.xml to dataset folder
                    ps2Info = os.path.join(path, "ps2-info" + "_" + plotID + ".xml")
                    os.rename(infoFile, ps2Info)  # rename info.xml
                    shutil.move(ps2Info, Datadir)


                # ==== Delete folders ====
                pathPos = os.path.join(subdirectories, filepose)


                if os.path.exists(path):
                    shutil.rmtree(path)
                if os.path.exists(pathPos):
                    shutil.rmtree(pathPos)

    except:
        print ('There is an ERROR in reading file dir: ') + path

    """finally:
        # ==== Delete folders ====
        pathPos = subdirectories + '/' + filepose

        if os.path.exists(path):
            shutil.rmtree(path)
        if os.path.exists(pathPos):
            shutil.rmtree(pathPos)"""