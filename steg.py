# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 17:49:37 2020

@author: user
"""


import click
from PIL import Image


class Steganography(object):
    @staticmethod
    def __int_to_bin(rgb):
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))
    
    @staticmethod
    def __bin_to_int(rgb):
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))
    
    @staticmethod
    #bits change
    def __merge_rgb(rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:1] + r2[:7],
               g1[:1] + g2[:7],
               b1[:1] + b2[:7])
        return rgb
    @staticmethod
    def merge(img1,img2):
            if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
                raise ValueError('Image 2 should not be larger than Image 1!')
                
            pixel_map1 = img1.load()
            pixel_map2 = img2.load()
            
            new_image = Image.new(img1.mode, img1.size)
            pixels_new = new_image.load()
            
            for i in range(img1.size[0]):
                for j in range(img1.size[1]):
                    rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])
                    
                    rgb2 = Steganography.__int_to_bin((0, 0, 0))
                    
                    if i < img2.size[0] and j < img2.size[1]:
                        rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])
                        
                    rgb = Steganography.__merge_rgb(rgb1, rgb2)
                    
                    pixels_new[i, j] = Steganography.__bin_to_int(rgb)
                    
            return new_image
        
        
        
    @staticmethod
    def unmerge(img):
            pixel_map = img.load()
            
            new_image = Image.new(img.mode, img.size)
            pixels_new = new_image.load()
            
            original_size = img.size
            
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    r, g, b = Steganography.__int_to_bin(pixel_map[i, j])
                    
                    rgb = (r[1:] + '0',
                           g[1:] + '0',
                           b[1:] + '0')
                    
                    pixels_new[i, j] = Steganography.__bin_to_int(rgb)
                    if pixels_new[i, j] != (0, 0, 0):
                        original_size = (i + 1, j + 1)
                        
                        
            new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
            
            return new_image
        
        
@click.group()
def cli():
    pass

@cli.command()
@click.option('--img1', required=True, type=str, help='Image that will hide another image')
@click.option('--img2', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='Output image')
def merge(img1, img2, output):
    merged_image = Steganography.merge(Image.open(img1), Image.open(img2))
    merged_image.save(output)
    
@cli.command()
@click.option('--img', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='Output image')
def unmerge(img, output):
    unmerged_image = Steganography.unmerge(Image.open(img))
    unmerged_image.save(output)
    
if __name__ == '__main__':
    cli()
    
    
                 

            
            
         
    
    
        
    
        
    
     
        
