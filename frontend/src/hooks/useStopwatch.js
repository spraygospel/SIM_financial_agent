// frontend/src/hooks/useStopwatch.js
import { useState, useRef, useCallback } from 'react';

export const useStopwatch = () => {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const timerRef = useRef(null);

  const start = useCallback(() => {
    if (isRunning) return;
    setIsRunning(true);
    const startTime = Date.now() - time;
    timerRef.current = setInterval(() => {
      setTime(Date.now() - startTime);
    }, 10); // Update setiap 10ms untuk tampilan yang mulus
  }, [isRunning, time]);

  const stop = useCallback(() => {
    if (!isRunning) return;
    setIsRunning(false);
    clearInterval(timerRef.current);
  }, [isRunning]);

  const reset = useCallback(() => {
    setTime(0);
    if (isRunning) {
      stop();
    }
  }, [isRunning, stop]);

  // Format waktu ke dalam format 00:00.000
  const formattedTime = new Date(time).toISOString().slice(14, 23);

  return { time, formattedTime, isRunning, start, stop, reset };
};