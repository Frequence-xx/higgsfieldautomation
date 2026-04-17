import React from 'react';
import {Composition} from 'remotion';
import {CaptionComposition} from './CaptionComposition';
import {PhoneUIComposition} from './PhoneUI';
import {Video3Main} from './Video3Testimonial';
import {BrotherTestimonial} from './BrotherVideo';
import video3Words from '../public/video3/words.json';

const procesWords = [
	{text: 'Een', startFrame: 0, endFrame: 5},
	{text: 'goede', startFrame: 7, endFrame: 15},
	{text: 'verhuizing', startFrame: 16, endFrame: 33},
	{text: 'begint', startFrame: 38, endFrame: 49},
	{text: 'met', startFrame: 50, endFrame: 54},
	{text: 'duidelijkheid.', startFrame: 56, endFrame: 82},
	{text: 'Binnen', startFrame: 121, endFrame: 131},
	{text: 'enkele', startFrame: 133, endFrame: 143},
	{text: 'minuten', startFrame: 145, endFrame: 160},
	{text: 'weten', startFrame: 166, endFrame: 176},
	{text: 'wij', startFrame: 176, endFrame: 179},
	{text: 'precies', startFrame: 181, endFrame: 192},
	{text: 'wat', startFrame: 194, endFrame: 197},
	{text: 'er', startFrame: 199, endFrame: 200},
	{text: 'nodig', startFrame: 201, endFrame: 211},
	{text: 'is.', startFrame: 213, endFrame: 225},
	{text: 'Daarna', startFrame: 258, endFrame: 275},
	{text: 'regelen', startFrame: 285, endFrame: 297},
	{text: 'we', startFrame: 298, endFrame: 301},
	{text: 'alles', startFrame: 303, endFrame: 312},
	{text: 'van', startFrame: 314, endFrame: 317},
	{text: 'planning', startFrame: 319, endFrame: 332},
	{text: 'tot', startFrame: 336, endFrame: 343},
	{text: 'uitvoering.', startFrame: 345, endFrame: 371},
	{text: 'Zonder', startFrame: 404, endFrame: 416},
	{text: 'verrassingen.', startFrame: 418, endFrame: 446},
];

const captionStyle = {
	fontFamily: 'Montserrat, sans-serif',
	fontSize: 52,
	color: '#FFFFFF',
	highlightColor: '#FC8434',
	strokeWidth: 6,
	strokeColor: '#000000',
	maxWordsPerLine: 3,
	maxLines: 2,
	verticalPosition: 0.60,
};

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition
				id="ProcesCaptions"
				component={CaptionComposition}
				durationInFrames={525}
				fps={30}
				width={1080}
				height={1920}
				defaultProps={{
					words: procesWords,
					style: captionStyle,
				}}
			/>
			<Composition
				id="PhoneUI"
				component={PhoneUIComposition}
				durationInFrames={90}
				fps={30}
				width={1080}
				height={1920}
			/>
			<Composition
				id="Video3Testimonial"
				component={Video3Main}
				durationInFrames={660}
				fps={30}
				width={1080}
				height={1920}
			/>
			<Composition
				id="BrotherTestimonial"
				component={BrotherTestimonial}
				durationInFrames={500}
				fps={30}
				width={1080}
				height={1920}
			/>
		</>
	);
};
