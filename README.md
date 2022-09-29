<h1><center> Image-Labeling</center></h1>

<h2>A tool for semi automated Image labeling</h2>
<br> 

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li>
        <a href="#intenal-working">Intenal working</a>
        <ul>
            <li><a href="#plugins">Plugins</a></li>
            <li><a href="#selection-algorithms">Selection Algorithms</a></li>
            <li><a href="#population-selection">Population Selection</a></li>
        </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
<br><br>

# About The Project
This tool can be used to label images given a set of reference image for each class. <br>
for ex : In case of tennis, we can label set of images as either Forehand, Backhand or Serve provided some reference images of each class.
Similarly this can be used for image labeling tasks in other domains too.

# Getting Started

## prerequisites
This tool requires python version of 3.8x and corresponding pip version. Use GPU for faster execution.
## Installation
<li>Step 1 : Clone the repository

`git clone https://github.com/AdityaVSM/Image-Labeling` </li>

<li>Step 2 : Change directory

`cd Image-Labeling` </li>

<li>Step 3 : Install requirements 

`pip3 install -r requirements.txt`</li>

# Usage
<li>Step 1: After installing the Required libraries,to view the supported plugins and algorithms use the below command 

`python main.py --help`


<li>Step 2: When the repository is cloned config.ymal file is downloaded.
out of the available plugins and algorithms chose the plugins and algorithms you wish for your domain and problem and modify the config.yaml file accordingly. Update the below fileds in the file
<ul>
    <li> 

`src_data_path` : path to the images that need to labelled</li>
    <li>
    `ref_data_path` : path of the reference images to label the test images </li>
    <li>
    `save_data_path` : path where the labelled images will be saved
    </li>
    <li>
    `src_data_mode` : It specifies if the path of the images is local or external link (currently supported mode is only local)
    </li>
</ul>
<li> Step 3: Run the main.py file</li>

<br>

# Contributing
Users can contibute to plugins, selection algorithm and population selection algoritms.
To contribute fork the repository and make changes in a seperate branch and raise a pull request

<li>Contributing to plugins</li>
<ul>
    <li>Name of class should be capitalized</li>
    <li>Inherit the PLUGIN abstract class</li>
    <li>Implement the comparision algorithm in
    
`compare_images(imageA, imageB)` function       which     returns the similarity score between      imageA and imageB</li>
    <li>Register the plugin in `.metadata.json`</li>
</ul>

<li> Contibuting to selection algorithms</li>
<ul>
    <li>Follow camel casing for class name</li>
    <li>Inherit Algorithms abstract class</li>
    <li>Implement the 

`get_res(plugins, img_path, ref_img_path)` function which should generate similarity from all pligins mentioned in config.yaml using `super().generate_scores(plugins,img_path, ref_img_path)` which return dictionary of results.
for ex the result for a tennis classification with 2 plugins and 3 classes looks like `{'orb': {'tennis\\backhand': 0.5586592178770949, 'tennis\\forehand': 0.5052083333333334, 'tennis\\serve': 0.4375}, 'ssim': {'tennis\\backhand': 0.4966169898362194, 'tennis\\forehand': 0.5442255631384915, 'tennis\\serve': 0.5371498091072633}}` Using this data obtain best result using your own custom algorithm</li>
    <li>Register the new filename and classname in 
`.metadata.json` Note that key should be all small cased and file name and class name should be alphabetically same as the one created</li>

</ul>


# Intenal working

## Plugins
This tool by default supports two plugins for image comaprion and labelling which are listed below

<li>ORB Similarity : It is a feature matching tool developed at opencv labs uses fusion of FAST keypoint detector and BRIEF descriptor for image comaprion and is used for image comparision and labelling.</li>

<li>SSIM similarity : It is another plugin suuported by the tool uses ssim for comapring a image with reference image and label the image</li>
<br>

## Selection Algorithms

These algorithms are used to classify the image to particular class using similarity scores of different plugins. One of such algorithm is implemneted by us.

<li>Highest Average Match: obtained by averaging over similarity score for different plugins for each class. From resulting scores the class with highest score is considered to be label fo that image.

<br>

## Population Selection

# License

# Acknowledgments



