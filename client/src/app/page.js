"use client";
import Link from "next/link";
import { useUser } from "@clerk/nextjs";

export default function Home() {
  const { user } = useUser();

  return (
    <main className="flex items-center justify-center p-20 flex-col">
      {user ? (
        null
      ) : ( <Link
          href={"/sign-up"}
          className="relative inline-flex h-10 overflow-hidden rounded-full p-[2px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50"
        >
          <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
          <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-950 px-3 py-1 text-sm font-medium text-white backdrop-blur-3xl">
            Sign up
          </span>
        </Link>)}

      <div id="documentation">
        <h1>Doucmentation</h1>
      </div>
      <div id="about-us">
        <h1>About Us</h1>
      </div>
    </main>
  );
}
