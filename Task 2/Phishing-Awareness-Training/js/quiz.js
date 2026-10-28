const quizQuestions = [
  {
    topic: "Email phishing",
    question: "An email claims your account will close in one hour and asks you to sign in using its link. What is the safest next step?",
    options: ["Click the link before the deadline", "Reply and ask whether it is real", "Open the official app or a trusted bookmark and check there", "Forward it to a friend to decide"],
    answer: 2,
    explanation: "Use a trusted route you already know. A link and an urgent deadline in an unexpected message are not a safe way to verify an account."
  },
  {
    topic: "Sender verification",
    question: "A familiar display name appears, but the full sender address has an unexpected spelling. What should you do?",
    options: ["Trust the display name", "Treat it as a warning sign and verify through a known channel", "Click the message link to see where it goes", "Send the email your password to confirm your identity"],
    answer: 1,
    explanation: "Display names can be misleading. Check the full address and confirm unexpected requests using a trusted, separate channel."
  },
  {
    topic: "Fake websites",
    question: "Which statement about HTTPS is accurate?",
    options: ["HTTPS proves the website belongs to a legitimate company", "HTTPS means the page cannot be a phishing page", "HTTPS encrypts the connection but does not prove the site is trustworthy", "HTTPS guarantees that a link in an email is safe"],
    answer: 2,
    explanation: "HTTPS protects data in transit, but a deceptive site can also use HTTPS. Verify the domain and navigate through a trusted route."
  },
  {
    topic: "Social engineering",
    question: "A caller claiming to be IT asks you to read out a one-time sign-in code. What should you do?",
    options: ["Share it because the caller knows your name", "Ask them to wait while you send the code by text", "Do not share it; end the call and contact IT using a known number", "Share only the first half of the code"],
    answer: 2,
    explanation: "One-time codes are secrets. Don’t share them with a caller; contact your support team through a trusted channel."
  },
  {
    topic: "Attachments",
    question: "You receive an unexpected attachment from a colleague. What is the safest response?",
    options: ["Open it because the sender is familiar", "Verify with the colleague using a separate trusted method before opening", "Disable security software and open it", "Forward it to everyone for review"],
    answer: 1,
    explanation: "A familiar account may be misused or compromised. Confirm an unexpected file out of band before opening it."
  },
  {
    topic: "Passwords",
    question: "A message asks for your password and verification code to prevent an account lockout. What should you do?",
    options: ["Provide them if the message looks professional", "Share the password but keep the code private", "Never share either; check the account independently and report the message", "Use the same password in the reply"],
    answer: 2,
    explanation: "Do not provide passwords or one-time codes in response to a message. Visit the service independently and report suspicious requests."
  },
  {
    topic: "MFA",
    question: "You receive an MFA approval prompt that you did not initiate. What is the safest action?",
    options: ["Approve it to make the notification stop", "Deny it and report the unexpected prompt through a trusted channel", "Share the prompt with a coworker to approve", "Ignore all future MFA prompts"],
    answer: 1,
    explanation: "An unrequested prompt may indicate someone is trying to sign in. Deny it and alert the service provider or your organization’s IT/security team."
  },
  {
    topic: "Payments",
    question: "A manager emails an urgent request to change a supplier’s bank details. What should you do?",
    options: ["Make the change immediately", "Reply asking for a second email", "Independently verify using a known contact method and follow payment controls", "Send a small test payment to check"],
    answer: 2,
    explanation: "Unexpected payment and account changes should be independently confirmed using a known number or established process, not contact details in the request."
  },
  {
    topic: "Reporting",
    question: "You identify a suspicious work email. What is the best action?",
    options: ["Forward it to coworkers as a warning", "Use your organization’s official report-phishing process or contact its security team", "Reply to the sender to investigate", "Post the full email and links publicly"],
    answer: 1,
    explanation: "Report it through your organization’s designated process. Avoid spreading suspicious links or interacting with the sender."
  },
  {
    topic: "Incident response",
    question: "You entered your password on a page you now suspect was fake. What should you do first?",
    options: ["Wait to see if anything happens", "Change it using the official site on a trusted device and promptly alert IT/security if it is a work account", "Send the password to IT by email", "Delete the browser history and take no further action"],
    answer: 1,
    explanation: "Act promptly: change the exposed password through the legitimate service, change it anywhere else it was reused, and tell your organization’s security team if relevant."
  }
];
