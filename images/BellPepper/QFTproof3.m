%%
clear all
close all
clc
%%
I = imread('28.jpg');
Pimiento_RGB = imcrop(I, [530 1030 2000 2500]);
[M, N] = size(Pimiento_RGB);
figure, 
imshow(Pimiento_RGB)
R_i = double(Pimiento_RGB(:,:,1));
G_j = double(Pimiento_RGB(:,:,2));
B_k = double(Pimiento_RGB(:,:,3));
%% 
ha = R_i;

FaFT = fft2(ha);
cFaFT = fftshift(FaFT);
pFaFT = abs(cFaFT);
figure,
imagesc(-floor(M/2):floor(M/2),-floor(N/2):floor(N/2),log(1+pFaFT)), axis xy % dibujamos el rango completo
title('Espectro de potencia R'), xlabel('frecuencias horizontales'), ylabel('frecuencias horizontales'),colorbar
%%
hb = G_j;

FbFT = fft2(hb);
cFbFT = fftshift(FbFT);
pFbFT = abs(cFbFT);
figure,
imagesc(-floor(M/2):floor(M/2),-floor(N/2):floor(N/2),log(1+pFbFT)), axis xy % dibujamos el rango completo
title('Espectro de potencia G'), xlabel('frecuencias horizontales'), ylabel('frecuencias horizontales'),colorbar
%%
hd = B_k;

FdFT = fft2(hd);
cFdFT = fftshift(FdFT);
pFdFT = abs(cFdFT);
figure,
imagesc(-floor(M/2):floor(M/2),-floor(N/2):floor(N/2),log(1+pFdFT)), axis xy % dibujamos el rango completo
title('Espectro de potencia B'), xlabel('frecuencias horizontales'), ylabel('frecuencias horizontales'),colorbar
%%
haproof = fft2(R_i);
hbproof = fft2(G_j + B_k);
r = zeros(size(haproof));
c = ones(size(haproof));
z = complex(r, c);

hbtemp = hbproof .* z;
%%
QFT = FaFT + hbtemp;
cQFT = fftshift(QFT);
pQFT = abs(cQFT);
figure,
imagesc(-floor(M/2):floor(M/2),-floor(N/2):floor(N/2),log(1+pQFT)), axis xy % dibujamos el rango completo
title('Espectro de potencia RGB'), xlabel('frecuencias horizontales'), ylabel('frecuencias horizontales'),colorbar
%%
H = fspecial('sobel');
H1 = filter2(H, pQFT);
H2 = filter2(transpose(H), pQFT);

Hedge = H1 .* H2;

QFTedge = ifft2(Hedge);
figure, 
imshow(QFTedge, [])