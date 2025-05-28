# keys will be displayed in the UI.
# Values must exactly match the related class names defined in the toolboxes.py file.
TOOLBOXES = {"BRIGHTNESS":
                {"NAME": "Brightness",
                 "CLASS": "BrightnessBox"},

             "SATURATION": 
                {"NAME": "Saturation",
                 "CLASS": "SaturationBox"},

             "CONTRAST":
                {"NAME": "Contrast",
                 "CLASS": "ContrastBox"},

             "FULL_SCALE_CONTRAST": 
                {"NAME": "Full Scale Contrast",
                 "CLASS": "FullScaleContrastBox"},

             "LOG":
                {"NAME": "Log Transform",
                 "CLASS": "LogBox"},

             "GAMMA":
                {"NAME": "Gamma Transform",
                 "CLASS": "GammaBox"},

             "RGB2GRAY": 
                {"NAME": "RGB to Gray",
                 "CLASS": "RGB2GrayBox"},

             "THRESHOLDING": 
                {"NAME": "Thresholding",
                 "CLASS": "ThresholdingBox"},

             "COMPLEMENT":  
                {"NAME": "Complement",
                 "CLASS": "ComplementBox"},

             "CROP": 
                {"NAME": "Crop",
                 "CLASS": "CropBox"},

             "FLIP":  
                {"NAME": "Flip",
                 "CLASS": "FlipBox"},

             "ROTATE": 
                {"NAME": "Rotate",
                 "CLASS": "RotateBox"},

             "RESIZE": 
                {"NAME": "Resize",
                 "CLASS": "ResizeBox"},

             "PADDING": 
                {"NAME": "Padding",
                 "CLASS": "PaddingBox"},

             "HISTEQ": 
                {"NAME": "Histogram Equalization",
                 "CLASS": "HistEqualizationBox"},

             "HISTCLAHE": 
                {"NAME": "Local Hist. Equalization",
                 "CLASS": "HistCLAHEBox"}, 

             "COLOR_MASKING": 
                {"NAME": "Color Masking",
                 "CLASS": "ColorMaskBox"},

             "SPATIAL_MASKING":  
                {"NAME": "Spatial Masking",
                 "CLASS": "SpatialMaskBox"},

             "BITSLICE": 
                {"NAME": "Bit Plane Slicing",
                 "CLASS": "BitSliceBox"},

             "ADD_NOISE": 
                {"NAME": "Add Noise",
                 "CLASS": "NoiseBox"},

             "ARITHMETIC": 
                {"NAME": "Image Arithmetic",
                 "CLASS": "ArithmeticBox"},

             "LOGIC": 
                {"NAME": "Image Logic",
                 "CLASS": "LogicBox"},

             "LAPLACE": 
                {"NAME": "Laplacian Filter",
                 "CLASS": "LaplaceBox"},

             "SOBEL": 
                {"NAME": "Sobel Filter",
                 "CLASS": "SobelBox"},

             "ORDER_STAT": 
                {"NAME": "Order Statistic Filter",
                 "CLASS": "OrderStatBox"},

             "SMOOTHING": 
                {"NAME": "Smoothing Filter",
                 "CLASS": "SmoothingBox"},

             "SHARPENING": 
                {"NAME": "Sharpening Filter",
                 "CLASS": "SharpeningBox",}}



# default channel names for the image.
CHANNEL_NAMES = ["Red", "Green", "Blue", "Alpha"]


# main button names
OPEN_BUTTON = "Open"
HISTOGRAM_BUTTON = "Histogram"
CHANNELS_BUTTON = "Channels"
FREQUENCY_BUTTON = "Frequency"
SAVE_BUTTON = "Save"


# title of the 'add new' toolbox
ADD_TOOLBOX_TITLE = "Add New"