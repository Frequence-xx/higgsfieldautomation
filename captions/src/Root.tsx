import React from 'react';
import {Composition} from 'remotion';
import {CaptionComposition} from './CaptionComposition';
import {PhoneUIComposition} from './PhoneUI';

// Word timestamps based on 11.1s voiceover starting at 0.5s in final video
// At 30fps: frame = seconds * 30
const vzzWords = [
	{text: 'Verhuizen', startFrame: 15, endFrame: 33},
	{text: 'zonder', startFrame: 33, endFrame: 45},
	{text: 'zorgen.', startFrame: 45, endFrame: 63},
	{text: 'Wij', startFrame: 75, endFrame: 81},
	{text: 'pakken', startFrame: 81, endFrame: 93},
	{text: 'het', startFrame: 93, endFrame: 99},
	{text: 'vakkundig', startFrame: 99, endFrame: 117},
	{text: 'in,', startFrame: 117, endFrame: 126},
	{text: 'vervoeren', startFrame: 135, endFrame: 153},
	{text: 'het', startFrame: 153, endFrame: 159},
	{text: 'veilig', startFrame: 159, endFrame: 174},
	{text: 'en', startFrame: 174, endFrame: 180},
	{text: 'leveren', startFrame: 180, endFrame: 195},
	{text: 'het', startFrame: 195, endFrame: 201},
	{text: 'met', startFrame: 201, endFrame: 207},
	{text: 'zorg', startFrame: 207, endFrame: 219},
	{text: 'af.', startFrame: 219, endFrame: 228},
	{text: 'Snel', startFrame: 255, endFrame: 270},
	{text: 'verhuizen.', startFrame: 270, endFrame: 294},
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
	verticalPosition: 0.62,
};

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition
				id="VZZCaptions"
				component={CaptionComposition}
				durationInFrames={450}
				fps={30}
				width={1080}
				height={1920}
				defaultProps={{
					words: vzzWords,
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
		</>
	);
};
