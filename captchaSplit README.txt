captcha folder contains raw margonem captcha
captchaSplitted contains raw captcha splitted into 6 parts and the top left letter has been removed
captchaMissingUnique, captchaNormalUnique, captchaUpsideDownUnique contain original images that have been approved by human


ORDER OF ACTIONS:
1. Get an image into 'captcha' folder
2. Run 'handleCaptchaAndMoveToFolders.py' script
3. Manually copy appropriate images from 'captchaSplitted' to 'captchaMissingUnique', 'captchaNormalUnique' or/and 'captchaUpsideDownUnique'
4. Run 'handleCaptchaAndMoveToFolders.py' script again
5. Train your CNN model