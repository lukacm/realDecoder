function [ circuit ] = readReal( file )
%READREAL Summary of this function goes here
%   Detailed explanation goes here
CNOT = [1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0];
CCNOT = [1 0 0 0 0 0 0 0; 0 1 0 0 0 0 0 0; 0 0 1 0 0 0 0 0; 0 0 0 1 0 0 0 0; 0 0 0 0 1 0 0 0; 0 0 0 0 0 1 0 0; 0 0 0 0 0 0 0 1; 0 0 0 0 0 0 1 0];
CV = [ 1 0 0 0; 0 1 0 0; 0 0 (1+j)/2 (1-j)/2; 0 0 (1-j)/2 (1+j)/2];


end

