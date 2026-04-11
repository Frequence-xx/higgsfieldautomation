import React from 'react';
import {
	AbsoluteFill,
	useCurrentFrame,
	useVideoConfig,
	spring,
	interpolate,
} from 'remotion';

export const PhoneUIComposition: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Phone slide-up animation
	const phoneSlide = spring({
		frame,
		fps,
		config: {damping: 14, stiffness: 120},
	});

	// Text fade-in staggered
	const titleOpacity = interpolate(frame, [10, 20], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const field1Opacity = interpolate(frame, [18, 28], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const field2Opacity = interpolate(frame, [24, 34], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const buttonScale = spring({
		frame: frame - 30,
		fps,
		config: {damping: 10, stiffness: 180},
	});

	// Hook text at bottom
	const hookOpacity = interpolate(frame, [40, 50], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill
			style={{
				backgroundColor: '#F5F0EB',
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			{/* Phone frame */}
			<div
				style={{
					transform: `translateY(${interpolate(phoneSlide, [0, 1], [200, 0])}px)`,
					opacity: phoneSlide,
					width: 380,
					height: 760,
					backgroundColor: '#FFFFFF',
					borderRadius: 40,
					border: '8px solid #1A1A1A',
					overflow: 'hidden',
					boxShadow: '0 30px 60px rgba(0,0,0,0.15)',
					display: 'flex',
					flexDirection: 'column' as const,
					alignItems: 'center',
					padding: '60px 30px 40px',
				}}
			>
				{/* Notch */}
				<div
					style={{
						position: 'absolute' as const,
						top: 12,
						width: 120,
						height: 28,
						backgroundColor: '#1A1A1A',
						borderRadius: 14,
					}}
				/>

				{/* App Logo */}
				<div
					style={{
						opacity: titleOpacity,
						marginTop: 20,
						marginBottom: 40,
					}}
				>
					<div
						style={{
							fontSize: 32,
							fontFamily: 'Montserrat, sans-serif',
							fontWeight: 900,
							color: '#FC8434',
							letterSpacing: '0.02em',
						}}
					>
						SNELVERHUIZEN.NL
					</div>
					<div
						style={{
							fontSize: 14,
							color: '#888',
							textAlign: 'center' as const,
							marginTop: 4,
						}}
					>
						Verhuizen zonder zorgen
					</div>
				</div>

				{/* Form fields */}
				<div
					style={{
						width: '100%',
						opacity: field1Opacity,
						marginBottom: 16,
					}}
				>
					<div
						style={{
							fontSize: 12,
							color: '#666',
							marginBottom: 6,
							fontFamily: 'Montserrat, sans-serif',
							fontWeight: 600,
						}}
					>
						HUIDIG ADRES
					</div>
					<div
						style={{
							height: 48,
							backgroundColor: '#F5F5F5',
							borderRadius: 10,
							border: '1px solid #DDD',
						}}
					/>
				</div>

				<div
					style={{
						width: '100%',
						opacity: field2Opacity,
						marginBottom: 16,
					}}
				>
					<div
						style={{
							fontSize: 12,
							color: '#666',
							marginBottom: 6,
							fontFamily: 'Montserrat, sans-serif',
							fontWeight: 600,
						}}
					>
						NIEUW ADRES
					</div>
					<div
						style={{
							height: 48,
							backgroundColor: '#F5F5F5',
							borderRadius: 10,
							border: '1px solid #DDD',
						}}
					/>
				</div>

				<div
					style={{
						width: '100%',
						opacity: field2Opacity,
						marginBottom: 30,
					}}
				>
					<div
						style={{
							fontSize: 12,
							color: '#666',
							marginBottom: 6,
							fontFamily: 'Montserrat, sans-serif',
							fontWeight: 600,
						}}
					>
						VERHUISDATUM
					</div>
					<div
						style={{
							height: 48,
							backgroundColor: '#F5F5F5',
							borderRadius: 10,
							border: '1px solid #DDD',
						}}
					/>
				</div>

				{/* CTA Button */}
				<div
					style={{
						width: '100%',
						transform: `scale(${Math.max(0, buttonScale)})`,
					}}
				>
					<div
						style={{
							height: 54,
							backgroundColor: '#FC8434',
							borderRadius: 12,
							display: 'flex',
							justifyContent: 'center',
							alignItems: 'center',
							boxShadow: '0 4px 12px rgba(252, 132, 52, 0.3)',
						}}
					>
						<span
							style={{
								fontSize: 16,
								fontFamily: 'Montserrat, sans-serif',
								fontWeight: 800,
								color: '#FFFFFF',
								letterSpacing: '0.04em',
							}}
						>
							PLAN JE VERHUIZING
						</span>
					</div>
				</div>
			</div>

			{/* Hook text below phone */}
			<div
				style={{
					position: 'absolute' as const,
					bottom: 180,
					opacity: hookOpacity,
					textAlign: 'center' as const,
				}}
			>
				<span
					style={{
						fontSize: 42,
						fontFamily: 'Montserrat, sans-serif',
						fontWeight: 900,
						color: '#1A1A1A',
						textTransform: 'uppercase' as const,
						WebkitTextStroke: '1px rgba(0,0,0,0.1)',
					}}
				>
					BINNEN MINUTEN
				</span>
				<br />
				<span
					style={{
						fontSize: 42,
						fontFamily: 'Montserrat, sans-serif',
						fontWeight: 900,
						color: '#FC8434',
						textTransform: 'uppercase' as const,
					}}
				>
					DUIDELIJKHEID
				</span>
			</div>
		</AbsoluteFill>
	);
};
