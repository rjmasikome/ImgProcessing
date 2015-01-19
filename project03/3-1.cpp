//
//  3-1.cpp
//  ImageProcessingProject3
//
//  Created by Maureen Tanuadji on 1/11/15.
//  Copyright (c) 2015 Maureen Tanuadji. All rights reserved.
//
#include <iostream>
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <math.h>

using namespace std;
using namespace cv;
#define _USE_MATH_DEFINES

struct Coefficient {
	float i1;
	float i2;
};
Coefficient cAlpha;
Coefficient cBeta;
Coefficient cGamma;
Coefficient cOmega;
float aPlus[4];
float aMinus[4];
float b[4];
Mat y, yP, yM;
float M_PI = 3.1415926;

void init(){
	cAlpha.i1 = 1.6800;
	cAlpha.i2 = -0.6803;
	cBeta.i1 = 3.7350;
	cBeta.i2 = -0.2598;
	cGamma.i1 = 1.7830;
	cGamma.i2 = 1.7230;
	cOmega.i1 = 0.6318;
	cOmega.i2 = 1.9970;
}
void calculateCoefficients(double sigma){
	float sincOmega1 = sin(cOmega.i1 / sigma);
	float sincOmega2 = sin(cOmega.i2 / sigma);
	float coscOmega1 = cos(cOmega.i1 / sigma);
	float coscOmega2 = cos(cOmega.i2 / sigma);
	float expcGamma1 = exp(-cGamma.i1 / sigma);
	float expcGamma2 = exp(-cGamma.i2 / sigma);
	aPlus[0] = cAlpha.i1 + cAlpha.i2;
	aPlus[1] = expcGamma2 * (cBeta.i2 * sincOmega2 - (cAlpha.i2 + 2 * cAlpha.i1) * coscOmega2);
	aPlus[1] = aPlus[1] + expcGamma1 * (cBeta.i1 * sincOmega1 - (2 * cAlpha.i2 + cAlpha.i1) * coscOmega1);
	aPlus[2] = 2 * expcGamma1 * expcGamma2 * ((cAlpha.i1 + cAlpha.i2) * coscOmega2 * coscOmega1 - coscOmega2 * cBeta.i1 * sincOmega1 - coscOmega1 * cBeta.i2 * sincOmega2);
	aPlus[2] = aPlus[2] + cAlpha.i2 * pow(expcGamma1, 2) + cAlpha.i1 * pow(expcGamma2, 2);
	aPlus[3] = expcGamma2 * pow(expcGamma1, 2) * (cBeta.i2 * sincOmega2 - cAlpha.i2 * coscOmega2);
	aPlus[3] = aPlus[3] + expcGamma1 * pow(expcGamma2, 2) * (cBeta.i1 * sincOmega1 - cAlpha.i1 * coscOmega1);

	b[0] = -2 * expcGamma2 * coscOmega2 - 2 * expcGamma1 * coscOmega1;
	b[1] = 4 * coscOmega2 * coscOmega1 * expcGamma1 * expcGamma2 + pow(expcGamma2, 2) + pow(expcGamma1, 2);
	b[2] = -2 * coscOmega1 * expcGamma1 * pow(expcGamma2, 2) - 2 * coscOmega2 * expcGamma2 * pow(expcGamma1, 2);
	b[3] = pow(expcGamma1, 2) * pow(expcGamma2, 2);

	int idx = 1;
	aMinus[idx - 1] = aPlus[1] - b[idx - 1] * aPlus[0]; idx++;//idx=1
	aMinus[idx - 1] = aPlus[2] - b[idx - 1] * aPlus[0]; idx++;//idx=2
	aMinus[idx - 1] = aPlus[3] - b[idx - 1] * aPlus[0]; idx++;//idx=3
	aMinus[idx - 1] = -b[idx - 1] * aPlus[0];//idx=4
}

void calculateYP(int i, int j, Mat _X, bool isRowDirection){
	float y1 = 0;
	float y2 = 0;
	for (int m = 0; m <= 3; m++) {
		float xTemp = 0;
		if (isRowDirection) {
			if (j - m >= 0){
				xTemp = _X.at<float>(i, j - m);
			}
		}
		else {
			if (i - m >= 0) {
				xTemp = _X.at<float>(i - m, j);
			}
		}
		y1 = y1 + aPlus[m] * xTemp;
	}
	for (int m = 1; m <= 4; m++) {
		float yTemp = 0;
		if (isRowDirection) {
			if (j - m >= 0)
			{
				yTemp = yP.at<float>(i, j - m);
			}
		}
		else {
			if (i - m >= 0)
			{
				yTemp = yP.at<float>(i - m, j);
			}
		}

		y2 = y2 + b[m - 1] * yTemp;
	}
	yP.at<float>(i, j) = y1 - y2;
}
void calculateYM(int i, int j, Mat _X, bool isRowDirection){
	float y1 = 0;
	float y2 = 0;
	for (int m = 1; m <= 4; m++) {
		float xTemp = 0;
		if (isRowDirection) {
			if (j + m<_X.cols){
				xTemp = _X.at<float>(i, j + m);
			}
		}
		else {
			if (i + m<_X.rows){
				xTemp = _X.at<float>(i + m, j);
			}
		}
		y1 = y1 + aMinus[m - 1] * xTemp;
	}
	for (int m = 1; m <= 4; m++) {
		float yTemp = 0;
		if (isRowDirection) {
			if (j + m<_X.cols){
				yTemp = yM.at<float>(i, j + m);
			}
		}
		else {
			if (i + m<_X.rows){
				yTemp = yM.at<float>(i + m, j);
			}
		}
		y2 = y2 + b[m - 1] * yTemp;
	}
	yM.at<float>(i, j) = y1 - y2;
}

int main(int argc, char** argv) {
	init();
	double e1 = getTickCount();
	//double sigmax= atof(argv[1]);
	float sigma = 20;
	calculateCoefficients(sigma);

	Mat imgSrc; Mat imgDest;
	imgSrc = imread("noise.jpg", 0); // 0 = CV_LOAD_IMAGE_GRAYSCALE

	char window_name1[] = "Unprocessed Image";
	char window_name2[] = "Processed Image";

	namedWindow(window_name1, WINDOW_AUTOSIZE);
	imshow("Unprocessed Image", imgSrc);

	y = Mat::zeros(imgSrc.rows, imgSrc.cols, CV_32FC1);
	Mat x;
	imgSrc.convertTo(x, CV_32FC1);

	for (int direction = 1; direction >= 0; direction--) {
		yP = Mat::zeros(imgSrc.rows, imgSrc.cols, CV_32FC1);
		yM = Mat::zeros(imgSrc.rows, imgSrc.cols, CV_32FC1);
		if (direction == 1){
			for (int i = 0; i<imgSrc.rows; i++) {
				for (int j = 0; j<imgSrc.cols; j++) {
					calculateYP(i, j, x, (bool)direction);
				}
				for (int j = imgSrc.cols - 1; j >= 0; j--) {
					calculateYM(i, j, x, (bool)direction);
				}

			}
		}
		else if (direction == 0){
			for (int j = 0; j<imgSrc.cols; j++) {
				for (int i = 0; i<imgSrc.rows; i++) {
					calculateYP(i, j, x, (bool)direction);
				}
				for (int i = imgSrc.rows - 1; i >= 0; i--) {
					calculateYM(i, j, x, (bool)direction);
				}
			}
		}
		float factor = 1.0 / (sigma * sqrt(2 * M_PI));
		for (int i = 0; i<imgSrc.rows; i++) {
			for (int j = 0; j<imgSrc.cols; j++) {
				y.at<float>(i, j) = (yP.at<float>(i, j) + yM.at<float>(i, j)) * factor;

			}
		}
		cv::normalize(y, x, 0, 255, NORM_MINMAX, CV_32FC1);
	}
	cv::normalize(y, imgDest, 0, 255, NORM_MINMAX, CV_8UC1);
	namedWindow(window_name2, WINDOW_AUTOSIZE);
	imshow("Processed Image", imgDest);

	//cout << "yP = "<< endl << " "  << yP << endl << endl;
	//cout << endl ;
	//cout << "yM = "<< endl  << " "  << yM << endl << endl;
	waitKey();
	double e2 = getTickCount();
	double time = e2 - e1;
	
	//return 0;
	cout << "Times passed in seconds: " << time << endl;
	
}