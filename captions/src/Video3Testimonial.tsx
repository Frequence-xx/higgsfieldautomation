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
import wordsPerShot from '../public/video3/words_per_shot.json';

const BRAND_ORANGE = '#FC8434';
const DARK_BG = '#0A0A0A';

// =============================================================
// S1 — Hook: ALL CAPS orange text on black
// =============================================================
export const S1Hook: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const textProgress = spring({
		frame: frame - 5,
		fps,
		config: {damping: 18, stiffness: 120},
	});

	const exitOpacity = interpolate(frame, [75, 89], [1, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill style={{backgroundColor: DARK_BG, opacity: exitOpacity}}>
			<div
				style={{
					position: 'absolute',
					top: '50%',
					left: '50%',
					transform: `translate(-50%, -50%) scale(${0.9 + 0.1 * textProgress})`,
					opacity: textProgress,
					textAlign: 'center',
					width: '90%',
					lineHeight: 1.1,
				}}
			>
				<div
					style={{
						fontFamily: 'Montserrat, sans-serif',
						fontWeight: 900,
						fontSize: 92,
						color: BRAND_ORANGE,
						textTransform: 'uppercase' as const,
						textShadow: '0 2px 20px rgba(252,132,52,0.3)',
						letterSpacing: '-0.005em',
					}}
				>
					WAT ALS JE VOORAF
					<br />
					DE <span style={{color: '#FFFFFF'}}>EXACTE PRIJS</span>
					<br />
					WIST?
				</div>
			</div>
		</AbsoluteFill>
	);
};

// =============================================================
// S5 — Offerte mockup: replica of real PDF (matches screenshot)
// =============================================================
export const S5OfferteMockup: React.FC = () => {
	const frame = useCurrentFrame();

	// Subtle zoom toward Totaal
	const zoomProgress = interpolate(frame, [0, 60], [1, 1.02], {
		extrapolateRight: 'clamp',
	});

	const phoneEntry = spring({
		frame,
		fps: 30,
		config: {damping: 16, stiffness: 140},
	});

	const ORG = BRAND_ORANGE;
	const GREY = '#6b6b6b';
	const DARK = '#1a1a1a';
	const LIGHT_BG = '#F5F5F5';
	const STATS_BG = '#FFF4EC';

	return (
		<AbsoluteFill
			style={{
				backgroundColor: '#121212',
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			<div
				style={{
					width: 820,
					height: 1650,
					backgroundColor: '#FFFFFF',
					borderRadius: 52,
					boxShadow: '0 20px 60px rgba(0,0,0,0.55), 0 0 0 14px #1a1a1a',
					overflow: 'hidden',
					transform: `translateY(${(1 - phoneEntry) * 100}px) scale(${zoomProgress})`,
					padding: '32px 38px',
					display: 'flex',
					flexDirection: 'column',
					fontFamily: 'Montserrat, sans-serif',
				}}
			>
				{/* ROW 1: Logo left | SNELVERHUIZEN center-right | Contact right */}
				<div style={{display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between'}}>
					<div style={{display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 0}}>
						<Img src={staticFile('video3/logo.png')} style={{width: 170, height: 'auto'}} />
						<div style={{fontWeight: 900, fontSize: 50, color: ORG, lineHeight: 1, marginTop: 4, letterSpacing: '-0.01em'}}>
							Offerte
						</div>
					</div>
					<div style={{fontWeight: 800, fontSize: 20, color: ORG, letterSpacing: '0.04em', marginTop: 16}}>
						SNELVERHUIZEN
					</div>
					<div style={{textAlign: 'right', fontSize: 11, color: GREY, lineHeight: 1.35, marginTop: 16}}>
						info@snelverhuizen.nl<br />
						Poortland 66, 1046 BD Amsterdam<br />
						085 333 11 33<br />
						KVK: 82905444
					</div>
				</div>

				{/* Orange divider */}
				<div style={{height: 2, backgroundColor: ORG, marginTop: 18, marginBottom: 16}} />

				{/* Order + Customer info */}
				<div style={{display: 'flex', gap: 20, fontSize: 12}}>
					<div style={{flex: 1}}>
						<div style={{color: GREY}}>Ordernummer</div>
						<div style={{fontWeight: 700, color: DARK, fontSize: 14}}>125698432</div>
						<div style={{color: GREY, marginTop: 8}}>Soort verhuizing</div>
					</div>
					<div style={{flex: 1.4}}>
						<div style={{display: 'grid', gridTemplateColumns: '80px 1fr', rowGap: 6, fontSize: 12}}>
							<div style={{color: GREY}}>Naam</div>
							<div style={{fontWeight: 700, color: DARK}}>T. de Vries</div>
							<div style={{color: GREY}}>Telefoon</div>
							<div style={{fontWeight: 600, color: DARK}}>06 12345678</div>
							<div style={{color: GREY}}>Email</div>
							<div style={{fontWeight: 600, color: DARK, fontSize: 11}}>t.devries@voorbeeld.nl</div>
							<div style={{color: GREY}}>Datum(s)</div>
							<div style={{fontWeight: 700, color: DARK}}>15 mrt 2026</div>
						</div>
					</div>
				</div>

				{/* Location rows (grey bg, orange labels) */}
				<LocationRow
					label="STARTLOCATIE VERHUIZERS"
					address="Vestigingsweg 12, 1234 AB Amsterdam"
					tone="light"
				/>
				<LocationRow
					label="ADRES 1"
					address="Bloemenkade 8, 1021 CD Amsterdam"
					sub="Begane grond · Lift: Nee · Parkeren: 5m"
				/>
				<LocationRow
					label="ADRES 2"
					address="Parkweg 45, 3581 EF Utrecht"
					sub="Tweede etage · Lift: Ja · Parkeren: 10m"
				/>
				<LocationRow
					label="EINDLOCATIE VERHUIZERS"
					address="Vestigingsweg 12, 1234 AB Amsterdam"
					tone="light"
				/>

				{/* Stats strip */}
				<div
					style={{
						marginTop: 12,
						padding: '10px 14px',
						backgroundColor: STATS_BG,
						display: 'grid',
						gridTemplateColumns: '1fr 1fr',
						gap: 6,
						fontSize: 11,
						borderRadius: 2,
					}}
				>
					<div>
						<span style={{color: GREY}}>Totale afstand: </span>
						<span style={{fontWeight: 700, color: DARK}}>38.4 KM</span>
					</div>
					<div>
						<span style={{color: GREY}}>Verwachte reistijd: </span>
						<span style={{fontWeight: 700, color: DARK}}>52 MIN</span>
					</div>
					<div>
						<span style={{color: GREY}}>Totaal volume: </span>
						<span style={{fontWeight: 700, color: DARK}}>18.00 m³</span>
					</div>
					<div>
						<span style={{color: GREY}}>Inlaad / Uitlaad: </span>
						<span style={{fontWeight: 700, color: DARK}}>75 / 60 min</span>
					</div>
				</div>

				{/* Pricing table */}
				<div style={{marginTop: 14, fontSize: 12}}>
					<div
						style={{
							display: 'grid',
							gridTemplateColumns: '2.2fr 0.7fr 0.8fr 0.5fr 0.8fr 0.9fr',
							gap: 6,
							padding: '8px 10px',
							backgroundColor: ORG,
							color: '#FFFFFF',
							fontWeight: 800,
							fontSize: 11,
							letterSpacing: '0.04em',
						}}
					>
						<div>BESCHRIJVING</div>
						<div style={{textAlign: 'right'}}>TIJD</div>
						<div style={{textAlign: 'right'}}>HVH</div>
						<div style={{textAlign: 'right'}}>M3</div>
						<div style={{textAlign: 'right'}}>€/EH</div>
						<div style={{textAlign: 'right'}}>TOTAAL</div>
					</div>
					<PriceRow6 desc="van start naar adres 1" tijd="12 Min" hvh="8.20 KM" m3="" peh="€ 0,91" totaal="€ 7,46" />
					<PriceRow6 desc="van adres 1 naar adres 2" tijd="45 Min" hvh="32.10 KM" m3="" peh="€ 0,91" totaal="€ 29,21" bg={LIGHT_BG} />
					<PriceRow6 desc="van adres 2 naar eind" tijd="52 Min" hvh="38.40 KM" m3="" peh="€ 0,91" totaal="€ 34,94" />
					<PriceRow6 desc="bus" tijd="4 Uur" hvh="1" m3="" peh="€ 35,00" totaal="€ 140,00" bg={LIGHT_BG} />
					<PriceRow6 desc="verhuizer" tijd="4 Uur" hvh="2" m3="" peh="€ 35,00" totaal="€ 280,00" />
					<PriceRow6 desc="Subtotaal" tijd="" hvh="" m3="" peh="" totaal="€ 491,61" bg="#FAFAFA" bold />
					<PriceRow6 desc="BTW (21%)" tijd="" hvh="" m3="" peh="" totaal="€ 103,24" bold />

					{/* TOTAAL row highlighted orange */}
					<div
						style={{
							marginTop: 2,
							padding: '12px 14px',
							backgroundColor: ORG,
							color: '#FFFFFF',
							display: 'grid',
							gridTemplateColumns: '1fr auto',
							fontWeight: 900,
							fontSize: 22,
							letterSpacing: '0.02em',
						}}
					>
						<div>Totaal</div>
						<div>€ 594,85</div>
					</div>
				</div>

				<div style={{marginTop: 12, fontSize: 9, color: GREY, lineHeight: 1.4}}>
					*Offerte is gebaseerd op pro forma concept. U betaalt altijd voor de daadwerkelijk gemaakte uren.
				</div>
			</div>
		</AbsoluteFill>
	);
};

// Helper — grey-bg location row
const LocationRow: React.FC<{label: string; address: string; sub?: string; tone?: 'light'}> = ({
	label,
	address,
	sub,
	tone,
}) => (
	<div
		style={{
			backgroundColor: tone === 'light' ? '#F5F5F5' : '#FAFAFA',
			padding: '8px 12px',
			marginTop: 6,
			borderLeft: `4px solid ${BRAND_ORANGE}`,
			fontSize: 12,
		}}
	>
		<div style={{color: BRAND_ORANGE, fontWeight: 800, fontSize: 10, letterSpacing: '0.05em'}}>
			{label}
		</div>
		<div style={{color: '#1a1a1a', fontWeight: 700, fontSize: 13, marginTop: 1}}>
			{address}
		</div>
		{sub && <div style={{color: '#6b6b6b', fontSize: 10.5, marginTop: 1}}>{sub}</div>}
	</div>
);

// Helper — 6-column pricing row
const PriceRow6: React.FC<{
	desc: string;
	tijd?: string;
	hvh?: string;
	m3?: string;
	peh?: string;
	totaal: string;
	bg?: string;
	bold?: boolean;
}> = ({desc, tijd, hvh, m3, peh, totaal, bg, bold}) => (
	<div
		style={{
			display: 'grid',
			gridTemplateColumns: '2.2fr 0.7fr 0.8fr 0.5fr 0.8fr 0.9fr',
			gap: 6,
			padding: '7px 10px',
			backgroundColor: bg ?? 'transparent',
			fontSize: 12,
			color: '#1a1a1a',
			fontWeight: bold ? 700 : 500,
		}}
	>
		<div>{desc}</div>
		<div style={{textAlign: 'right', color: '#666'}}>{tijd ?? ''}</div>
		<div style={{textAlign: 'right', color: '#666'}}>{hvh ?? ''}</div>
		<div style={{textAlign: 'right', color: '#666'}}>{m3 ?? ''}</div>
		<div style={{textAlign: 'right', color: '#666'}}>{peh ?? ''}</div>
		<div style={{textAlign: 'right', fontWeight: 700}}>{totaal}</div>
	</div>
);

// =============================================================
// S7 — CTA end card (with real logo)
// =============================================================
export const S7CTA: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const logoEntry = spring({frame, fps, config: {damping: 14, stiffness: 130}});
	const headlineEntry = spring({frame: frame - 8, fps, config: {damping: 18, stiffness: 120}});
	const urlEntry = spring({frame: frame - 18, fps, config: {damping: 20, stiffness: 110}});

	return (
		<AbsoluteFill
			style={{
				background: `linear-gradient(160deg, #0A0A0A 0%, #1A0D04 100%)`,
				justifyContent: 'center',
				alignItems: 'center',
				padding: 80,
			}}
		>
			{/* Real Snelverhuizen logo */}
			<div
				style={{
					transform: `scale(${0.5 + 0.5 * logoEntry})`,
					opacity: logoEntry,
					marginBottom: 60,
				}}
			>
				<Img src={staticFile('video3/logo.png')} style={{width: 520, height: 'auto'}} />
			</div>

			{/* Headline */}
			<div
				style={{
					fontFamily: 'Montserrat, sans-serif',
					fontWeight: 900,
					fontSize: 74,
					color: '#FFFFFF',
					textAlign: 'center',
					textTransform: 'uppercase' as const,
					lineHeight: 1.05,
					letterSpacing: '-0.005em',
					opacity: headlineEntry,
					transform: `translateY(${(1 - headlineEntry) * 30}px)`,
					marginBottom: 20,
				}}
			>
				ONTVANG DIRECT
				<br />
				<span style={{color: BRAND_ORANGE}}>JE PRIJSINDICATIE</span>
			</div>

			{/* URL pill */}
			<div
				style={{
					fontFamily: 'Montserrat, sans-serif',
					fontWeight: 800,
					fontSize: 54,
					color: '#FFFFFF',
					textTransform: 'uppercase' as const,
					textAlign: 'center',
					marginTop: 40,
					padding: '24px 56px',
					border: `4px solid ${BRAND_ORANGE}`,
					borderRadius: 100,
					opacity: urlEntry,
					transform: `translateY(${(1 - urlEntry) * 40}px) scale(${0.85 + 0.15 * urlEntry})`,
					letterSpacing: '0.01em',
				}}
			>
				SNELVERHUIZEN.NL
			</div>

			{/* Phone */}
			<div
				style={{
					fontFamily: 'Montserrat, sans-serif',
					fontWeight: 800,
					fontSize: 42,
					color: BRAND_ORANGE,
					marginTop: 30,
					opacity: urlEntry,
					letterSpacing: '0.08em',
				}}
			>
				085 333 11 33
			</div>
		</AbsoluteFill>
	);
};

// =============================================================
// Per-shot caption layer (uses LOCAL shot timing)
// =============================================================
const captionStyle = {
	fontFamily: 'Montserrat, sans-serif',
	fontSize: 52,
	color: '#FFFFFF',
	highlightColor: BRAND_ORANGE,
	strokeWidth: 6,
	strokeColor: '#000000',
	maxWordsPerLine: 3,
	maxLines: 2,
	verticalPosition: 1.05, // 3rd quarter vertical — CSS paddingTop % is width-relative, so 1.05 × 1080 = y=1134 (section 3 of 1920). Per Farouq 2026-04-16.
};

// =============================================================
// Main composition — per-shot captions prevent bleed-through
// =============================================================
export const Video3Main: React.FC = () => {
	const s2Words = (wordsPerShot as any).s2 ?? [];
	const s3Words = (wordsPerShot as any).s3 ?? [];
	const s4Words = (wordsPerShot as any).s4 ?? [];
	const s5Words = (wordsPerShot as any).s5 ?? [];
	const s6Words = (wordsPerShot as any).s6 ?? [];

	return (
		<AbsoluteFill style={{backgroundColor: '#000000'}}>
			{/* Nasheed background: steady 0.22 (-13dB, softer than -9dB per owner feedback — this nasheed mastered hotter), 3s fade-out only */}
			<Audio
				src={staticFile('video3/nasheed2_trimmed.mp3')}
				volume={(f) =>
					f < 570 ? 0.22 : interpolate(f, [570, 660], [0.22, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
				}
			/>

			{/* S1 Hook 0-90 (3s) — no SFX, silent hook */}
			<Sequence from={0} durationInFrames={90}>
				<S1Hook />
			</Sequence>

			{/* S2 Marco speaks 90-196 (3.55s) */}
			<Sequence from={90} durationInFrames={107}>
				<OffthreadVideo src={staticFile('video3/s2.mp4')} />
				<CaptionComposition words={s2Words} style={captionStyle} />
			</Sequence>

			{/* S3 Jolanda cutaway 196-294 (3.24s) */}
			<Sequence from={196} durationInFrames={98}>
				<OffthreadVideo src={staticFile('video3/s3.mp4')} muted />
				<Audio src={staticFile('video3/s3_audio.mp3')} />
				<CaptionComposition words={s3Words} style={captionStyle} />
			</Sequence>

			{/* S4 Marco speaks 294-436 (4.68s) — motion-smoothed 30fps to reduce stutter */}
			<Sequence from={294} durationInFrames={141}>
				<OffthreadVideo src={staticFile('video3/s4_smooth30.mp4')} />
				<CaptionComposition words={s4Words} style={captionStyle} />
			</Sequence>

			{/* S5 Offerte mockup 436-507 (2.35s) */}
			<Sequence from={436} durationInFrames={71}>
				<S5OfferteMockup />
				<Audio src={staticFile('video3/s5_audio.mp3')} />
				<Audio src={staticFile('video3/ui_tap_v2.mp3')} volume={0.35} />
				<CaptionComposition words={s5Words} style={captionStyle} />
			</Sequence>

			{/* S6 Marco closes 507-546 (1.23s) — Avatar Pro lipsync */}
			<Sequence from={507} durationInFrames={40}>
				<OffthreadVideo src={staticFile('video3/s6_lipsync.mp4')} />
				<CaptionComposition words={s6Words} style={captionStyle} />
			</Sequence>

			{/* S7 CTA 546-660 (3.8s) — no brand sting, ambient continues */}
			<Sequence from={546} durationInFrames={114}>
				<S7CTA />
			</Sequence>
		</AbsoluteFill>
	);
};
