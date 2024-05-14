'use client';
import Image from 'next/image';
import Link from 'next/link';
import { useUser } from '@clerk/nextjs';
import { UserButton } from "@clerk/clerk-react";
import { ModeToggle } from '../mode-toggle';
import {TypewriterEffectSmooth} from "@/components/ui/typewriter-effect"
const Navbar = () => {
    const { isLoaded, isSignedIn, user } = useUser();
    const words = [
      {
        text: "FRAMEWORK",
      },
      {
        text: "FOR",
      },
      {
        text: "TASK",
      },
      {
        text: "SCHEDULING",
      },
      {
        text: "USING",
      },
      {
        text: "LOGISTIC",
        className: "text-blue-500 dark:text-blue-500",
      },
      {
        text: "REGRESSION.",
        className: "text-blue-500 dark:text-blue-500",
      },
    ];
    const handleSignInClick = () => {
      if (!user) {
        window.location.href = '/sign-in'; // Redirect to the sign-in page
      }
    };

    return (
      <header className="fixed right-0 left-0 top-0 py-4 px-4 bg-black/40 backdrop-blur-lg z-[100] flex items-center border-b-[1px] border-neutral-900 justify-between">
        <aside className="flex items-center gap-[2px]">
        <TypewriterEffectSmooth  words={words} />
        </aside>
        <nav className="absolute left-[50%] top-[50%] transform translate-x-[-50%] translate-y-[-50%] hidden md:block">
          <ul className="flex items-center gap-4 list-none">
            <li>
              <Link href="/#about">About The Project</Link>
            </li>
            {user? <>
              <li>
                <Link href="/model">Model</Link>
              </li>
            </>:
            <>
            </>}
          </ul>
        </nav>
        <aside className="flex items-center gap-4">
          {/* <ModeToggle className="absolute inset-0" /> */}
          {isLoaded && (
            <>
              {isSignedIn ? (
                <UserButton />
              ) : (
                <button
                  onClick={handleSignInClick}
                  className="relative inline-flex h-10 overflow-hidden rounded-full p-[2px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50"
                ><span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
                <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-950 px-3 py-1 text-sm font-medium text-white backdrop-blur-3xl">
                  Sign in
                </span>
                </button>
              )}
            </>
          )}
        </aside>
      </header>
    );
};

export default Navbar;
