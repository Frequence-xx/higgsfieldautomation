import React from 'react';
import {Composition} from 'remotion';
import {CaptionComposition} from './CaptionComposition';

const defaultWords = [
	{text: 'Your', startFrame: 0, endFrame: 15},
	{text: 'move,', startFrame: 8, endFrame: 25},
	{text: 'done', startFrame: 20, endFrame: 35},
	{text: 'right.', startFrame: 30, endFrame: 50},
];

const defaultStyle = {
	fontFamily: 'Playfair Display, Georgia, serif',
	fontSize: 64,
	color: '#FFFFFF',
	highlightColor: '#FFD700',
	position: 'lower-third' as const,
	animation: 'spring' as const,
};

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition
				id="Captions"
				component={CaptionComposition}
				durationInFrames={186}
				fps={30}
				width={1920}
				height={1080}
				defaultProps={{
					words: defaultWords,
					style: defaultStyle,
					platformFormat: '16:9' as const,
				}}
			/>
			<Composition
				id="CaptionsVertical"
				component={CaptionComposition}
				durationInFrames={186}
				fps={30}
				width={1080}
				height={1920}
				defaultProps={{
					words: defaultWords,
					style: defaultStyle,
					platformFormat: '9:16' as const,
				}}
			/>
			<Composition
				id="CaptionsSquare"
				component={CaptionComposition}
				durationInFrames={186}
				fps={30}
				width={1080}
				height={1080}
				defaultProps={{
					words: defaultWords,
					style: defaultStyle,
					platformFormat: '1:1' as const,
				}}
			/>
		</>
	);
};
