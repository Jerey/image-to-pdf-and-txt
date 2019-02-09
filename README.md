# Image to text and PDF

I enjoy the thrive to the paperless world, as I find it much easier organizing digital documents. But since many documents are still required as a hardcopy, one is still forced to archive those.

In order to reduce the amount of time spent organizing those documents, I bought a numbering stamp. This stamp automatically increases the number with each stamping. It is put on each document. Then I take a picture of all documents. After that, the images are organized in folders by the name of the number on the document. Then a python script is started with the path to the images. This script takes one to many images per document, tries to align them in a way that the text is "as horizontal as possible". This is done, since one easily is off by a few degrees when taking pictures with a camera or a phone. Then the slightly rotated images are stored to a pdf and used to extract text from them. This text then is stored to txt-files. The hardcopy documents are now simply archived in order of the number of the stamp. Whenever I now need a certain document, I can simply search for it on the computer and it will tell me, which number the document has.

## Installation

### Docker Build

Go to the folder where the Dockerfile is located and execute following command:

```docker build -t image-to-pdf-txt```

### Manually

It is also possible to install the dependencies for the python script by yourself:

1. Go to the folder, where the project is located.
2. ```pip install -r requirements.txt```
3. Install the packages ```tesseract-ocr``` and ```tesseract-ocr-deu```.  

The ```tesseract-ocr-deu``` package is required to have German language support. There are several others, which can be added.

## Running the script

Again, it is possible to run the script manually or via Docker.

In general, the script does four steps:
1. Collect a list of pdfs to be produced.
2. Rotate the image. Often the text is a bit skew, if one takes the images by hand, through which the OCR result tends to be worse.
3. Extract the text and store it to a text file.
4. Takt eh rotated images and store it to a pdf.

### Docker Run

The script allows you to either define a folder, where the images are located in, or directly provide the path to the images.

When using docker, it is advisible to use the default command, which uses the folder option.

```docker run --rm -it -v $(pwd)/convert:/app/convert:ro -v $(pwd)/result:/app/result image-to-pdf-txt```

The two volumes/directories used in the docker script are:

- ```result```: This is where the text files and the PDFs are stored to.
- ```convert```: This is the folder, where the images, which shall be converted, are located at.

The script uses your current working directory.

### Python

Using the manually installed version, one can simply use ```python3 main.py -f convert```.

## Functions

The script currently has to ways of being used: By providing a folder, where the images to be converted is given, or by providing the images in the command line.

### Folder option

The folder option takes one folder and searches recursively for images. The expected input is a folder, where subfolders are given including the images and each subfolder represents one document. For each subfolder, a pdf and a txt file is created. See following example:

```
convert
|
|─0001
| | Img1.jpg
| | Img2.jpg
|
|─0002
| | Img3.jpg
|
|─0003
  | Img4.jpg
  | Img5.jpg
  | Img6.jpg
```

When passing the folder "convert" to the script, the output would be as follows:

```
result
| 0001.txt -> Contains the extracted text from Img1.jpg and Img2.jpg.
| 0001.pdf -> Contains the images Img1.jpg and Img2.jpg.
| 0002.txt -> Contains the extracted text from Img3.jpg.
| 0002.pdf -> Contains the images Img3.jpg.
| 0003.txt -> Contains the extracted text from Img4.jpg, Img5.jpg and Img6.jpg.
| 0003.pdf -> Contains the images Img4.jpg, Img5.jpg and Img6.jpg.
```

The order of the images in the folder is sorted by name. So the PDF and the text document will keep the order of names. (e.g. Img4 is followed by Img5 and then Img6, despite the creation date).

### Image option

The image option allows you to directly pass the images to the python script. It is also possible to define one to many pages per document:

```python3 main.py -i folder/Img1.jpg,folder/Img2.jpg -i folder/Img3.jpg -i folder/Img4.jpg,folder/Img5.jpg,folder/Img6.jpg```

The output would be as followed:

```
result
| Img1.txt -> Contains the extracted text from Img1.jpg and Img2.jpg.
| Img1.pdf -> Contains the images Img1.jpg and Img2.jpg.
| Img3.txt -> Contains the extracted text from Img3.jpg.
| Img3.pdf -> Contains the images Img3.jpg.
| Img4.txt -> Contains the extracted text from Img4.jpg, Img5.jpg and Img6.jpg.
| Img4.pdf -> Contains the images Img4.jpg, Img5.jpg and Img6.jpg.
```

Using the image flage, the order is not based on the name, but rather on the order provided to the script.

## Drawback

1. The image must have a good resolution and the text must be well readable, otherwise the output will not be all that great. In that case, it is possible that searching fails. But it is possible to add descriptive names to the number of the folder name through which manual searching can be improved.

## Credits

Since I was completely new to Python, being a C++ developer, and further being new to OCR, I had search my way through the internet to help me create this tool. The [Py Image Search-Page](https://www.pyimagesearch.com/) helped me a lot, specifically the blog entry about [the text skew correction](https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/). The text skew pretty was pretty much taken from that entry, with some minor adaptions.
