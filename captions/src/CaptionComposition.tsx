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
	const activeWordIndex = words.findIndex(
		(w) => frame >= w.startFrame && frame <= w.endFrame
	);

	// If no word is active, check if we're in a silence gap
	if (activeWordIndex < 0) {
		// Find the last word that ended before current frame
		const lastSpokenIndex = words.reduce((last, w, i) =>
			frame > w.endFrame ? i : last, -1);

		// If no words spoken yet, hide
		if (lastSpokenIndex < 0) return null;

		// If we're past the last word entirely, hide (prevents bleed into CTA)
		if (lastSpokenIndex === words.length - 1 && frame > words[lastSpokenIndex].endFrame + 15) {
			return null;
		}

		// Check if gap between last word and next word is > 30 frames (1 second) = silence gap, hide
		const nextWordIndex = lastSpokenIndex + 1;
		if (nextWordIndex < words.length) {
			const gap = words[nextWordIndex].startFrame - words[lastSpokenIndex].endFrame;
			if (gap > 30 && frame > words[lastSpokenIndex].endFrame + 10) {
				return null; // Hide during long silence gaps
			}
		}
	}

	// Find effective index for page calculation
	const currentIndex = activeWordIndex >= 0
		? activeWordIndex
		: words.reduce((last, w, i) => frame > w.endFrame ? i : last, -1);

	if (currentIndex < 0) return null;

	const effectiveIndex = Math.max(0, currentIndex);

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
										letterSpacing: '0.03em',
										WebkitTextStroke: `4px ${style.strokeColor}`,
										paintOrder: 'stroke fill',
										textShadow: '0 2px 8px rgba(0,0,0,0.6), 0 4px 16px rgba(0,0,0,0.3), 2px 2px 4px rgba(0,0,0,0.4)',
										opacity: enterProgress,
										transform: `scale(${0.85 + 0.15 * enterProgress})`,
										// Orange highlight background on active word
										backgroundColor: isActive
											? style.highlightColor
											: 'transparent',
										padding: isActive ? '6px 14px' : '4px 4px',
										borderRadius: '8px',
										transition: 'background-color 0.08s ease',
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
