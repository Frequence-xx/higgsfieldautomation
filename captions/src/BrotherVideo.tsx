import React from 'react';
import {
	AbsoluteFill,
	Audio,
	Img,
	OffthreadVideo,
	Sequence,
	interpolate,
	spring,
	staticFile,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import {CaptionComposition} from './CaptionComposition';
import brotherWords from '../public/video3/brother_words.json';

const BRAND_ORANGE = '#FC8434';

const captionStyle = {
	fontFamily: 'Montserrat, sans-serif',
	fontSize: 52,
	color: '#FFFFFF',
	highlightColor: BRAND_ORANGE,
	strokeWidth: 6,
	strokeColor: '#000000',
	maxWordsPerLine: 3,
	maxLines: 2,
	verticalPosition: 1.05,
};

// Text overlay with selective orange word highlighting
// Use {} delimiters in text to mark orange words: "Plain {orange} more"
const TextOverlay: React.FC<{text: string}> = ({text}) => {
	const frame = useCurrentFrame();
	const {fps, durationInFrames} = useVideoConfig();

	const fadeIn = interpolate(frame, [0, 15], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const fadeOut = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const alpha = Math.min(fadeIn, fadeOut);
	const textEntry = spring({frame: frame - 8, fps, config: {damping: 18, stiffness: 120}});

	// Parse text — segments inside {} are orange, others white
	const parts = text.split(/(\{[^}]+\})/g).filter(Boolean);

	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: 80, opacity: alpha}}>
			<div
				style={{
					fontFamily: 'Montserrat, sans-serif',
					fontWeight: 900,
					fontSize: 76,
					color: '#FFFFFF',
					textAlign: 'center',
					textTransform: 'uppercase' as const,
					lineHeight: 1.1,
					letterSpacing: '-0.005em',
					opacity: textEntry,
					transform: `translateY(${(1 - textEntry) * 30}px)`,
					textShadow: '0 4px 24px rgba(0,0,0,0.8)',
					WebkitTextStroke: '3px #000000',
					paintOrder: 'stroke fill' as const,
				}}
			>
				{parts.map((p, i) => {
					if (p.startsWith('{') && p.endsWith('}')) {
						return (
							<span key={i} style={{color: BRAND_ORANGE}}>
								{p.slice(1, -1)}
							</span>
						);
					}
					return <span key={i}>{p}</span>;
				})}
			</div>
		</AbsoluteFill>
	);
};

// Crossfade wrapper (defined here so it's available for both Shot2 + CTA)
const FadeTransition: React.FC<{children: React.ReactNode; inFrames?: number; outFrames?: number}> = ({
	children,
	inFrames = 15,
	outFrames = 15,
}) => {
	const frame = useCurrentFrame();
	const {durationInFrames} = useVideoConfig();
	const fadeIn = inFrames > 0
		? interpolate(frame, [0, inFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
		: 1;
	const fadeOut = outFrames > 0
		? interpolate(frame, [durationInFrames - outFrames, durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
		: 1;
	return <AbsoluteFill style={{opacity: Math.min(fadeIn, fadeOut)}}>{children}</AbsoluteFill>;
};

// CTA end card
const CTAEndCard: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const logoEntry = spring({frame, fps, config: {damping: 14, stiffness: 130}});
	const line1Entry = spring({frame: frame - 10, fps, config: {damping: 18, stiffness: 120}});
	const line2Entry = spring({frame: frame - 22, fps, config: {damping: 20, stiffness: 110}});

	return (
		<AbsoluteFill
			style={{
				backgroundColor: '#FFFFFF',
				justifyContent: 'center',
				alignItems: 'center',
				padding: 60,
			}}
		>
			{/* Paper texture as single Img layer at 5% opacity */}
			{/* texture removed per Farouq 2026-04-17 */}
			<div
				style={{
					transform: `scale(${0.7 + 0.3 * logoEntry})`,
					opacity: logoEntry,
					marginBottom: 50,
				}}
			>
				<Img src={staticFile('video3/logo.png')} style={{width: 500, height: 'auto'}} />
			</div>
			<div
				style={{
					fontFamily: 'Montserrat, sans-serif',
					fontWeight: 900,
					fontSize: 72,
					color: '#1a1a1a',
					textAlign: 'center',
					textTransform: 'uppercase' as const,
					lineHeight: 1.05,
					letterSpacing: '-0.01em',
					opacity: line1Entry,
					transform: `translateY(${(1 - line1Entry) * 30}px)`,
					marginBottom: 30,
				}}
			>
				GEEN GEDOE.
				<br />
				<span style={{color: BRAND_ORANGE}}>GEWOON GEREGELD.</span>
			</div>
			<div
				style={{
					fontFamily: 'Montserrat, sans-serif',
					fontWeight: 600,
					fontSize: 36,
					color: '#4a4a4a',
					textAlign: 'center',
					lineHeight: 1.3,
					opacity: line2Entry,
					transform: `translateY(${(1 - line2Entry) * 20}px)`,
					marginTop: 30,
				}}
			>
				Binnen enkele minuten je offerte.
				<br />
				<span style={{fontWeight: 800, color: '#1a1a1a'}}>Vrijblijvend.</span>
			</div>
			<div
				style={{
					fontFamily: 'Montserrat, sans-serif',
					fontWeight: 800,
					fontSize: 40,
					color: '#FFFFFF',
					backgroundColor: BRAND_ORANGE,
					textTransform: 'uppercase' as const,
					textAlign: 'center',
					marginTop: 50,
					padding: '18px 42px',
					borderRadius: 100,
					opacity: line2Entry,
					transform: `translateY(${(1 - line2Entry) * 30}px) scale(${0.9 + 0.1 * line2Entry})`,
					letterSpacing: '0.02em',
					boxShadow: '0 10px 30px rgba(252,132,52,0.3)',
				}}
			>
				SNELVERHUIZEN.NL
			</div>
		</AbsoluteFill>
	);
};

// Shot 2 — skip ~2.3s of source (startFrom=70). 210-70=140f available (4.67s) — needed to fit ANTWOORD 1s longer + no CTA overlap. Strict 3s skip would force black gap.
const Shot2WithGradient: React.FC = () => {
	return (
		<AbsoluteFill style={{overflow: 'hidden'}}>
			<OffthreadVideo src={staticFile('video3/brother_pan.mp4')} muted startFrom={70} />
			<div
				style={{
					position: 'absolute',
					inset: 0,
					background: 'linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 30%)',
				}}
			/>
		</AbsoluteFill>
	);
};

// =============================================================
// Main 20s composition (per Farouq clarification)
// 0-300 (0-10s):    Shot 1 brother speaks (video has audio + ambient)
// 300-330 (10-11s): brief crossfade transition (still on shot 1 video tail)
// 330-495 (11-16.5s): BLURRED shot 2 as bg + VRAAG (330-405) + ANTWOORD (420-495) overlays
// 495-510 (16.5-17s): crossfade
// 510-600 (17-20s): CTA end card
// Ambient bed: continues throughout (already in shot 1 video, plus extend with file)
// =============================================================
export const BrotherTestimonial: React.FC = () => {
	return (
		<AbsoluteFill style={{backgroundColor: '#000000'}}>
			{/* 0-280: shot 1 (9.33s) with QUICK 10f fade-out at end */}
			<Sequence from={0} durationInFrames={280}>
				<FadeTransition inFrames={0} outFrames={10}>
					<OffthreadVideo src={staticFile('video3/brother15_v15.mp4')} />
				</FadeTransition>
				<CaptionComposition words={brotherWords as any} style={captionStyle} />
			</Sequence>

			{/* 270-410: shot 2 (140f, startFrom=70). 10f crossfade with shot 1 ending */}
			<Sequence from={270} durationInFrames={140}>
				<FadeTransition inFrames={10} outFrames={0}>
					<Shot2WithGradient />
				</FadeTransition>
			</Sequence>

			{/* VRAAG 9-11s (60f) — 1s earlier */}
			<Sequence from={270} durationInFrames={60}>
				<TextOverlay text="Wil jij ook een verhuizing zonder {gedoe en stress}?" />
			</Sequence>

			{/* ANTWOORD 11-13.67s (80f) — 1s earlier + 1s longer */}
			<Sequence from={330} durationInFrames={80}>
				<TextOverlay text="Dan wil je dat het {gewoon goed geregeld} is." />
			</Sequence>

			{/* Continuous ambient — plays from frame 0 throughout entire composition for seamless audio bed (no gap when shot 1 audio ends). Very low volume to layer subtly under shot 1's existing ambient. */}
			<Audio src={staticFile('video3/ambient_clean.mp3')} volume={0.025} loop />

			{/* CTA starts direct after shot 2 ends at 410. Duration 3s (90f) */}
			<Sequence from={410} durationInFrames={90}>
				<FadeTransition inFrames={0} outFrames={15}>
					<CTAEndCard />
				</FadeTransition>
			</Sequence>
		</AbsoluteFill>
	);
};
