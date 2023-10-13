import os
import captchaSplit
import cv2
import shutil

def remove_letters(input_string):
    return ''.join([char for char in input_string if not char.isalpha()])

def moveImageFromDirToDir(sourceFolder, destinationFolder, filename):
    source_path = os.path.normpath(os.path.join(sourceFolder + '/', filename))
    destination_path = os.path.normpath(os.path.join(destinationFolder + '/', filename))

    # Check if the source image exists
    if os.path.exists(source_path):
        try:
            # Move the image from source folder to destination folder
            shutil.move(source_path, destination_path)
            #print(f"Image '{filename}' moved successfully.")
        except Exception as e:
            print(f"Error moving image: {str(e)}")
    else:
        print(f"Image '{filename}' not found in the source folder.")
def splitTrainIntoValidateAndTest(trainFolder, validateFolder, testFolder):
    missing = [f for f in os.listdir(trainFolder) if
                         os.path.isfile(os.path.join(trainFolder, f))]
    moveImageCounter = -1
    for img in missing:
        moveImageCounter += 1
        if moveImageCounter == 0:
            #print('move to validate folder')
            moveImageFromDirToDir(trainFolder, validateFolder, img)
        elif moveImageCounter == 7:
            #print('move to test folder')
            moveImageFromDirToDir(trainFolder, testFolder, img)
        elif moveImageCounter > 7:
            moveImageCounter = -1


def removeFilesFromDirectory(directoryPath):
    for filename in os.listdir(directoryPath):
        file_path = os.path.normpath(os.path.join(directoryPath + '/', filename))
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete file
            elif os.path.isdir(file_path):
                os.rmdir(file_path)  # Delete empty subfolder
            else:
                print(f"Skipping: {file_path} (unknown file type)")
        except Exception as e:
            print(f"Error deleting: {file_path} - {str(e)}")

#captchaSplit.split_image("captcha/1.jpg", "captchaSplitted"); #"captcha/1.jpg", "captchaSplitted"
if __name__ == "__main__":
    rawCaptchaFolder = "captcha"  # Replace with the path to your input folder
    splitCaptchaFolder = "captchaSplitted"

    missingCaptchaFolderUnique = "captchaMissingUnique"
    missingTrainFolder = "TrainData/missingFolder"
    missingValidateFolder = 'ValidateData/missingFolder'
    missingTestFolder = 'TestData/missingFolder'

    upsideDownCaptchaFolderUnique = "captchaUpsideDownUnique"
    upsideDownTrainFolder = "TrainData/upsideDownFolder"
    upsideDownValidateFolder = 'ValidateData/upsideDownFolder'
    upsideDownTestFolder = 'TestData/upsideDownFolder'

    normalCaptchaFolderUnique = "captchaNormalUnique"
    normalTrainFolder = "TrainData/normalFolder"
    normalValidateFolder = 'ValidateData/normalFolder'
    normalTestFolder = 'TestData/normalFolder'


    # List all files in the input folder
    rawCaptcha = [f for f in os.listdir(rawCaptchaFolder) if os.path.isfile(os.path.join(rawCaptchaFolder, f))]
    #when having files that are named different than number.jpg this code is mandatory
    rawCaptchaFileNames = []
    for captcha in rawCaptcha:
        captchaFileName = captcha.split('.')[0]
        captchaExtention = captcha.split('.')[1]
        if not any(c.isalpha() for c in captchaFileName) and captchaExtention == 'jpg': # if filename doesnt contain letters
            rawCaptchaFileNames.append(int(captchaFileName))
    print('max raw captcha number is: ', max(rawCaptchaFileNames))
    maxCaptchaFileNameNumber = max(rawCaptchaFileNames)

    for captcha in rawCaptcha:
        captchaFileName = captcha.split('.')[0]
        captchaExtention = captcha.split('.')[1]
        #print(captchaExtention)
        if any(c.isalpha() for c in captchaFileName) and captchaExtention == 'jpg':
            os.rename(rawCaptchaFolder + '/' + captcha, rawCaptchaFolder + '/' + str(maxCaptchaFileNameNumber+1)+'.jpg')
            print('rename ', captcha, ' to ', str(maxCaptchaFileNameNumber+1)+'.jpg')
            maxCaptchaFileNameNumber += 1
    #exit()
    rawCaptcha = [f for f in os.listdir(rawCaptchaFolder) if os.path.isfile(os.path.join(rawCaptchaFolder, f))]
    rawCaptchaIndexes = [remove_letters(os.path.splitext(os.path.basename(captcha))[0]) for captcha in rawCaptcha]
    #print('rawCaptchaIndexes: ',rawCaptchaIndexes)

    splittedCaptcha = [f for f in os.listdir(splitCaptchaFolder) if os.path.isfile(os.path.join(splitCaptchaFolder, f))]
    #remove redundant letters from array (if theres more than 1 same string)

    splittedCaptchaIndexes = [remove_letters(os.path.splitext(os.path.basename(captcha))[0]) for captcha in splittedCaptcha]
    splittedCaptchaIndexes = list(set(splittedCaptchaIndexes)) #unique values - shrinked 6 times

    #print('splittedCaptchaIndexes: ', splittedCaptchaIndexes)

    newCaptchas = 0
    for captcha in rawCaptchaIndexes:
        if captcha in splittedCaptchaIndexes:
            continue
        newCaptchas += 1

    count = 0
    for captcha in rawCaptcha:
        fileName = remove_letters(os.path.splitext(os.path.basename(captcha))[0])
        if fileName in splittedCaptchaIndexes:
            #print('file ', fileName, ' found in the array. Skipping.')
            continue
        else:
            count += 1
            print('Processing raw captchas ', count, '/', newCaptchas)
            captchaSplit.captchaSplit(rawCaptchaFolder, splitCaptchaFolder, fileName)
    print('Processed ', count, ' raw captchas and created ', count*6, 'new elements.\n\n')




    #but first clear target folders to prevent adding duplicate data
    removeFilesFromDirectory(missingTrainFolder)
    removeFilesFromDirectory(missingValidateFolder)
    removeFilesFromDirectory(missingTestFolder)

    removeFilesFromDirectory(upsideDownTrainFolder)
    removeFilesFromDirectory(upsideDownValidateFolder)
    removeFilesFromDirectory(upsideDownTestFolder)

    removeFilesFromDirectory(normalTrainFolder)
    removeFilesFromDirectory(normalValidateFolder)
    removeFilesFromDirectory(normalTestFolder)

    #*** missing captchas
    missingCaptchaUnique = [f for f in os.listdir(missingCaptchaFolderUnique) if os.path.isfile(os.path.join(missingCaptchaFolderUnique, f))]
    # precount
    newCaptchas = 0
    for captcha in missingCaptchaUnique:
        captchaFileName = captcha.split('.')[0]
        if not os.path.exists(missingTrainFolder + '/' + captcha):
            newCaptchas += 1
        if not os.path.exists(missingTrainFolder + '/' + captchaFileName + 'MirroredY.jpg'):
            newCaptchas += 1
        if not os.path.exists(missingTrainFolder + '/' + captchaFileName + 'MirroredX.jpg'):
            newCaptchas += 1
        if not os.path.exists(missingTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg'):
            newCaptchas += 1

    count = 1
    for captcha in missingCaptchaUnique:
        image = cv2.imread(missingCaptchaFolderUnique + "/" + captcha)
        captchaFileName = captcha.split('.')[0]
        if not os.path.exists(missingTrainFolder + '/' + captcha):
            cv2.imwrite(missingTrainFolder + '/' + captcha, image)
            print('Creating <missing> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(missingTrainFolder + '/' + captchaFileName + 'MirroredY.jpg'):
            flipped_imageY = cv2.flip(image, 1)
            cv2.imwrite(missingTrainFolder + '/' + captchaFileName + 'MirroredY.jpg', flipped_imageY)
            print('Creating <missing> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(missingTrainFolder + '/' + captchaFileName + 'MirroredX.jpg'):
            flipped_imageX = cv2.flip(image, 0)
            cv2.imwrite(missingTrainFolder + '/' + captchaFileName + 'MirroredX.jpg', flipped_imageX)
            print('Creating <missing> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(missingTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg'):
            flipped_imageXY = cv2.flip(image, -1)
            cv2.imwrite(missingTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg', flipped_imageXY)
            print('Creating <missing> flip copy ', count, '/', newCaptchas)
            count += 1
    print('Created ', count - 1, ' new captcha variants from <missing> captchas.\n\n')




    # *** normal captchas
    normalCaptchaUnique = [f for f in os.listdir(normalCaptchaFolderUnique) if
                     os.path.isfile(os.path.join(normalCaptchaFolderUnique, f))]
    # precount
    newCaptchas = 0
    for captcha in normalCaptchaUnique:
        captchaFileName = captcha.split('.')[0]
        if not os.path.exists(normalTrainFolder + '/' + captcha):
            newCaptchas += 1
        if not os.path.exists(normalTrainFolder + '/' + captchaFileName + 'MirroredY.jpg'):
            newCaptchas += 1
        if not os.path.exists(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredX.jpg'):
            newCaptchas += 1
        if not os.path.exists(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg'):
            newCaptchas += 1

    count = 1
    for captcha in normalCaptchaUnique:
        image = cv2.imread(normalCaptchaFolderUnique + "/" + captcha)
        captchaFileName = captcha.split('.')[0]
        if not os.path.exists(normalTrainFolder + '/' + captcha):
            cv2.imwrite(normalTrainFolder + '/' + captcha, image)
            print('Creating <normal> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(normalTrainFolder + '/' + captchaFileName + 'MirroredY.jpg'):
            flipped_imageY = cv2.flip(image, 1)
            cv2.imwrite(normalTrainFolder + '/' + captchaFileName + 'MirroredY.jpg', flipped_imageY)
            print('Creating <normal> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredX.jpg'):
            flipped_imageX = cv2.flip(image, 0)
            cv2.imwrite(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredX.jpg', flipped_imageX)
            print('Creating <normal> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg'):
            flipped_imageXY = cv2.flip(image, -1)
            cv2.imwrite(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg', flipped_imageXY)
            print('Creating <normal> flip copy ', count, '/', newCaptchas)
            count += 1
    print('Created ', count - 1, ' new captcha variants from <normal> captchas.\n\n')




    # *** upsideDown captcha
    upsideDownCaptchaUnique = [f for f in os.listdir(upsideDownCaptchaFolderUnique) if
                         os.path.isfile(os.path.join(upsideDownCaptchaFolderUnique, f))]
    # precount
    newCaptchas = 0
    for captcha in upsideDownCaptchaUnique:
        captchaFileName = captcha.split('.')[0]
        if not os.path.exists(upsideDownTrainFolder + '/' + captcha):
            newCaptchas += 1
        if not os.path.exists(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredY.jpg'):
            newCaptchas += 1
        if not os.path.exists(normalTrainFolder + '/' + captchaFileName + 'MirroredX.jpg'):
            newCaptchas += 1
        if not os.path.exists(normalTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg'):
            newCaptchas += 1

    count = 1
    for captcha in upsideDownCaptchaUnique:
        image = cv2.imread(upsideDownCaptchaFolderUnique + "/" + captcha)
        captchaFileName = captcha.split('.')[0]
        if not os.path.exists(upsideDownTrainFolder + '/' + captcha):
            cv2.imwrite(upsideDownTrainFolder + '/' + captcha, image)
            print('Creating <upsideDown> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredY.jpg'):
            flipped_imageY = cv2.flip(image, 1)
            cv2.imwrite(upsideDownTrainFolder + '/' + captchaFileName + 'MirroredY.jpg', flipped_imageY)
            print('Creating <upsideDown> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(normalTrainFolder + '/' + captchaFileName + 'MirroredX.jpg'):
            flipped_imageX = cv2.flip(image, 0)
            cv2.imwrite(normalTrainFolder + '/' + captchaFileName + 'MirroredX.jpg', flipped_imageX)
            print('Creating <upsideDown> flip copy ', count, '/', newCaptchas)
            count += 1

        if not os.path.exists(normalTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg'):
            flipped_imageXY = cv2.flip(image, -1)
            cv2.imwrite(normalTrainFolder + '/' + captchaFileName + 'MirroredXY.jpg', flipped_imageXY)
            print('Creating <upsideDown> flip copy ', count, '/', newCaptchas)
            count += 1
    print('Created ', count - 1, ' new captcha variants from <upsideDown> captchas.\n')

    ## after operations above, get 7th element to test and validate folders, it equals around 70%, 15%, 15% distribution ---!! currently ~78% ~11% 11%



    #distribute missing images to train, validate, test
    splitTrainIntoValidateAndTest(missingTrainFolder, missingValidateFolder, missingTestFolder)

    # distribute upsideDown images to train, validate, test
    splitTrainIntoValidateAndTest(upsideDownTrainFolder, upsideDownValidateFolder, upsideDownTestFolder)

    # distribute normal images to train, validate, test
    splitTrainIntoValidateAndTest(normalTrainFolder, normalValidateFolder, normalTestFolder)

