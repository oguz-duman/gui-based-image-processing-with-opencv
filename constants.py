# keys will be displayed in the UI.
# Values must exactly match the related class names defined in the toolboxes.py file.
TOOLBOXES = {"BRIGHTNESS":
                {"NAME": "Brightness",
                 "METHOD": "BrightnessBox"},

             "SATURATION": 
                {"NAME": "Saturation",
                 "METHOD": "SaturationBox"},

             "CONTRAST":
                {"NAME": "Contrast",
                 "METHOD": "ContrastBox"},

             "FULL_SCALE_CONTRAST": 
                {"NAME": "Full Scale Contrast",
                 "METHOD": "FullScaleContrastBox"},

             "LOG":
                {"NAME": "Log Transform",
                 "METHOD": "LogBox"},

             "GAMMA":
                {"NAME": "Gamma Transform",
                 "METHOD": "GammaBox"},

             "RGB2GRAY": 
                {"NAME": "RGB to Gray",
                 "METHOD": "RGB2GrayBox"},

             "THRESHOLDING": 
                {"NAME": "Thresholding",
                 "METHOD": "ThresholdingBox"},

             "COMPLEMENT":  
                {"NAME": "Complement",
                 "METHOD": "ComplementBox"},

             "CROP": 
                {"NAME": "Crop",
                 "METHOD": "CropBox"},

             "FLIP":  
                {"NAME": "Flip",
                 "METHOD": "FlipBox"},

             "ROTATE": 
                {"NAME": "Rotate",
                 "METHOD": "RotateBox"},

             "RESIZE": 
                {"NAME": "Resize",
                 "METHOD": "ResizeBox"},

             "PADDING": 
                {"NAME": "Padding",
                 "METHOD": "PaddingBox"},

             "HISTEQ": 
                {"NAME": "Histogram Equalization",
                 "METHOD": "HistEqualizationBox"},

             "HISTCLAHE": 
                {"NAME": "Local Hist. Equalization",
                 "METHOD": "HistCLAHEBox"}, 

             "COLOR_MASKING": 
                {"NAME": "Color Masking",
                 "METHOD": "ColorMaskBox"},

             "SPATIAL_MASKING":  
                {"NAME": "Spatial Masking",
                 "METHOD": "SpatialMaskBox"},

             "BITSLICE": 
                {"NAME": "Bit Plane Slicing",
                 "METHOD": "BitSliceBox"},

             "ADD_NOISE": 
                {"NAME": "Add Noise",
                 "METHOD": "NoiseBox"},

             "ARITHMETIC": 
                {"NAME": "Image Arithmetic",
                 "METHOD": "ArithmeticBox"},

             "LOGIC": 
                {"NAME": "Image Logic",
                 "METHOD": "LogicBox"},

             "LAPLACE": 
                {"NAME": "Laplacian Filter",
                 "METHOD": "LaplaceBox"},

             "SOBEL": 
                {"NAME": "Sobel Filter",
                 "METHOD": "SobelBox"},

             "ORDER_STAT": 
                {"NAME": "Order Statistic Filter",
                 "METHOD": "OrderStatBox"},

             "SMOOTHING": 
                {"NAME": "Smoothing Filter",
                 "METHOD": "SmoothingBox"},

             "SHARPENING": 
                {"NAME": "Sharpening Filter",
                 "METHOD": "SharpeningBox",}}



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