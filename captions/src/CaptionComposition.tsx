import React from 'react';
import {
	AbsoluteFill,
	useCurrentFrame,
	useVideoConfig,
	interpolate,
	spring,
} from 'remotion';

type Word = {
	text: string;
	startFrame: number;
	endFrame: number;
};

type CaptionStyle = {
	fontFamily: string;
	fontSize: number;
	color: string;
	highlightColor: string;
	position: 'lower-third' | 'center' | 'upper-third';
	animation: 'fade' | 'spring' | 'reveal';
};

type PlatformFormat = '9:16' | '1:1' | '16:9';

export const CaptionComposition: React.FC<{
	words: Word[];
	style: CaptionStyle;
	platformFormat: PlatformFormat;
}> = ({words, style, platformFormat}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const safeMargin = platformFormat === '9:16' ? 120 : 60;
	const bottomOffset =
		style.position === 'lower-third'
			? safeMargin
			: style.position === 'center'
				? undefined
				: undefined;
	const topOffset = style.position === 'upper-third' ? safeMargin : undefined;

	return (
		<AbsoluteFill
			style={{
				justifyContent:
					style.position === 'center' ? 'center' : 'flex-end',
				alignItems: 'center',
				paddingBottom: bottomOffset,
				paddingTop: topOffset,
			}}
		>
			<div
				style={{
					display: 'flex',
					flexWrap: 'wrap',
					justifyContent: 'center',
					gap: '8px',
					maxWidth: '80%',
				}}
			>
				{words.map((word, i) => {
					const isActive =
						frame >= word.startFrame && frame <= word.endFrame;
					const hasAppeared = frame >= word.startFrame;

					let opacity = 0;
					let scale = 1;

					if (style.animation === 'fade') {
						opacity = interpolate(
							frame,
							[word.startFrame - 3, word.startFrame],
							[0, 1],
							{extrapolateRight: 'clamp', extrapolateLeft: 'clamp'},
						);
					} else if (style.animation === 'spring') {
						const spr = spring({
							frame: frame - word.startFrame,
							fps,
							config: {damping: 12, stiffness: 200},
						});
						opacity = hasAppeared ? 1 : 0;
						scale = hasAppeared ? spr : 0;
					} else {
						opacity = hasAppeared ? 1 : 0;
					}

					return (
						<span
							key={i}
							style={{
								fontFamily: style.fontFamily,
								fontSize: style.fontSize,
								fontWeight: 700,
								color: isActive ? style.highlightColor : style.color,
								opacity,
								transform: `scale(${scale})`,
								textShadow: '2px 2px 8px rgba(0,0,0,0.7)',
								letterSpacing: '0.02em',
								transition: 'color 0.1s ease',
							}}
						>
							{word.text}
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
