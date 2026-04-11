import React from 'react';
import {
	AbsoluteFill,
	useCurrentFrame,
	useVideoConfig,
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
	strokeWidth: number;
	strokeColor: string;
	maxWordsPerLine: number;
	maxLines: number;
	verticalPosition: number; // 0-1, where captions sit on screen
};

export const CaptionComposition: React.FC<{
	words: Word[];
	style: CaptionStyle;
}> = ({words, style}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Group words into pages (max lines × max words per line)
	const maxWordsPerPage = style.maxLines * style.maxWordsPerLine;

	// Find which words are currently visible based on timing
	// Show a "page" of words: the group containing the currently active word
	const activeWordIndex = words.findIndex(
		(w) => frame >= w.startFrame && frame <= w.endFrame
	);

	// If no word is active, find the last word that was spoken
	const currentIndex = activeWordIndex >= 0
		? activeWordIndex
		: words.findIndex((w) => frame < w.startFrame) - 1;

	if (currentIndex < 0 && activeWordIndex < 0) {
		return null; // No captions to show yet
	}

	const effectiveIndex = Math.max(0, currentIndex >= 0 ? currentIndex : activeWordIndex);

	// Calculate which page of words we're on
	const pageIndex = Math.floor(effectiveIndex / maxWordsPerPage);
	const pageStart = pageIndex * maxWordsPerPage;
	const pageEnd = Math.min(pageStart + maxWordsPerPage, words.length);
	const pageWords = words.slice(pageStart, pageEnd);

	// Only show the page if at least one word has started
	if (frame < pageWords[0]?.startFrame) {
		return null;
	}

	// Split page words into lines
	const lines: Word[][] = [];
	for (let i = 0; i < pageWords.length; i += style.maxWordsPerLine) {
		lines.push(pageWords.slice(i, i + style.maxWordsPerLine));
	}

	return (
		<AbsoluteFill
			style={{
				justifyContent: 'flex-start',
				alignItems: 'center',
				paddingTop: `${style.verticalPosition * 100}%`,
			}}
		>
			<div
				style={{
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					gap: '8px',
				}}
			>
				{lines.map((lineWords, lineIndex) => (
					<div
						key={`line-${pageIndex}-${lineIndex}`}
						style={{
							display: 'flex',
							flexWrap: 'nowrap',
							justifyContent: 'center',
							gap: '10px',
						}}
					>
						{lineWords.map((word, wordIndex) => {
							const hasAppeared = frame >= word.startFrame;
							const isActive =
								frame >= word.startFrame && frame <= word.endFrame;

							// Spring animation for word appearance
							const enterProgress = hasAppeared
								? spring({
										frame: frame - word.startFrame,
										fps,
										config: {damping: 15, stiffness: 200},
									})
								: 0;

							return (
								<span
									key={`${pageIndex}-${lineIndex}-${wordIndex}`}
									style={{
										fontFamily: style.fontFamily,
										fontSize: style.fontSize,
										fontWeight: 900,
										color: style.color,
										textTransform: 'uppercase' as const,
										letterSpacing: '0.02em',
										WebkitTextStroke: `${style.strokeWidth}px ${style.strokeColor}`,
										paintOrder: 'stroke fill',
										textShadow: '3px 3px 6px rgba(0,0,0,0.5)',
										opacity: enterProgress,
										transform: `scale(${0.8 + 0.2 * enterProgress})`,
										// Orange highlight background on active word
										backgroundColor: isActive
											? style.highlightColor
											: 'transparent',
										padding: isActive ? '4px 12px' : '4px 4px',
										borderRadius: '6px',
										transition: 'background-color 0.05s ease',
									}}
								>
									{word.text}
								</span>
							);
						})}
					</div>
				))}
			</div>
		</AbsoluteFill>
	);
};
