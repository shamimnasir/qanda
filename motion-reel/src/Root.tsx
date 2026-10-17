import React from 'react';
import {Composition} from 'remotion';
import {Identity, IDENTITY_DURATION} from './compositions/Identity';
import {VIDEO} from './theme';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Identity"
        component={Identity}
        durationInFrames={IDENTITY_DURATION}
        fps={VIDEO.fps}
        width={VIDEO.width}
        height={VIDEO.height}
      />
    </>
  );
};
