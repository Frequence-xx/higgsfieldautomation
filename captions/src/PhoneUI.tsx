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
				backgroundColor: '#1A1A1A',
				justifyContent: 'center',
				alignItems: 'center',
				backgroundImage: 'radial-gradient(ellipse at center, rgba(252,132,52,0.15) 0%, rgba(26,26,26,0.95) 70%)',
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

				{/* Logo + Brand */}
				<div
					style={{
						opacity: titleOpacity,
						marginTop: 20,
						marginBottom: 30,
						display: 'flex',
						flexDirection: 'column' as const,
						alignItems: 'center',
						gap: '8px',
						padding: '0 20px',
					}}
				>
					{/* Snelverhuizen logo */}
					<img
						src={require('/opt/pipeline/captions/public/logo.png')}
						style={{
							width: 200,
							height: 'auto',
						}}
					/>
					<div
						style={{
							fontSize: 13,
							color: '#888',
							textAlign: 'center' as const,
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

			{/* CTA text below phone */}
			<div
				style={{
					position: 'absolute' as const,
					bottom: 200,
					opacity: hookOpacity,
					textAlign: 'center' as const,
					padding: '0 40px',
				}}
			>
				<span
					style={{
						fontSize: 36,
						fontFamily: 'Montserrat, sans-serif',
						fontWeight: 900,
						color: '#FFFFFF',
						textTransform: 'uppercase' as const,
						WebkitTextStroke: '2px rgba(0,0,0,0.3)',
						paintOrder: 'stroke fill',
						textShadow: '0 2px 8px rgba(0,0,0,0.5)',
					}}
				>
					START JE AANVRAAG
				</span>
				<br />
				<span
					style={{
						fontSize: 20,
						fontFamily: 'Montserrat, sans-serif',
						fontWeight: 600,
						color: '#FFFFFF',
						marginTop: 8,
						display: 'inline-block',
						WebkitTextStroke: '1px rgba(0,0,0,0.2)',
						paintOrder: 'stroke fill',
						opacity: 0.9,
					}}
				>
					085 3331133 • snelverhuizen.nl
				</span>
			</div>
		</AbsoluteFill>
	);
};
