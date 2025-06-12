# A2A Friend Scheduling - System Architecture Diagrams

## 1. Host Agent Tools and Data Flow

```mermaid
flowchart TD
    User[User Interface] --> HostAgent[Host Agent]
    
    subgraph "Host Agent Tools"
        HostAgent --> Tool1[list_host_availability]
        HostAgent --> Tool2[book_host_meeting] 
        HostAgent --> Tool3[manage_host_availability]
        HostAgent --> Tool4[send_message]
    end
    
    subgraph "Host Schedule Database"
        HostSchedule[(HOST_SCHEDULE)]
        Tool1 --> HostSchedule
        Tool2 --> HostSchedule
        Tool3 --> HostSchedule
    end
    
    subgraph "A2A Communication"
        Tool4 --> A2AClient[A2A Client]
        A2AClient --> HTTP[HTTP Request]
    end
    
    subgraph "Remote Agents"
        HTTP --> Karley[Karley Coaching Services<br/>Port 10002]
        HTTP --> Nate[Nate Agent<br/>Port 10003] 
        HTTP --> Kaitlynn[Kaitlynn Agent<br/>Port 10004]
    end
    
    subgraph "Remote Agent Tools"
        Karley --> KarleyTool[get_availability]
        Nate --> NateTool[get_availability]
        Kaitlynn --> KaitlynnTool[get_availability]
    end
    
    subgraph "Remote Calendars"
        KarleyTool --> KarleySchedule[(Coaching Schedule)]
        NateTool --> NateSchedule[(Personal Calendar)]
        KaitlynnTool --> KaitlynnSchedule[(Personal Calendar)]
    end
    
    %% Return Data Flow
    KarleySchedule --> KarleyTool
    NateSchedule --> NateTool  
    KaitlynnSchedule --> KaitlynnTool
    
    KarleyTool --> Karley
    NateTool --> Nate
    KaitlynnTool --> Kaitlynn
    
    Karley --> A2AResponse[A2A Response]
    Nate --> A2AResponse
    Kaitlynn --> A2AResponse
    
    A2AResponse --> A2AClient
    A2AClient --> Tool4
    Tool4 --> HostAgent
    HostAgent --> User
    
    %% Styling
    classDef hostTool fill:#e1f5fe
    classDef remoteTool fill:#fff3e0
    classDef database fill:#f3e5f5
    classDef communication fill:#e8f5e8
    
    class Tool1,Tool2,Tool3,Tool4 hostTool
    class KarleyTool,NateTool,KaitlynnTool remoteTool
    class HostSchedule,KarleySchedule,NateSchedule,KaitlynnSchedule database
    class A2AClient,HTTP,A2AResponse communication
```

## 2. A2A Protocol Communication Sequence

```mermaid
sequenceDiagram
    participant User
    participant HostAgent as Host Agent
    participant A2AClient as A2A Client
    participant RemoteAgent as Remote Agent
    participant RemoteExecutor as Agent Executor
    participant RemoteTool as get_availability
    participant Calendar as Agent Calendar
    
    User->>HostAgent: "Schedule meeting for next 3 days"
    
    Note over HostAgent: Host checks own availability first
    HostAgent->>HostAgent: list_host_availability("2025-06-13")
    HostAgent->>HostAgent: list_host_availability("2025-06-14") 
    HostAgent->>HostAgent: list_host_availability("2025-06-15")
    
    Note over HostAgent: Send availability requests to friends
    loop For each friend agent
        HostAgent->>A2AClient: send_message(agent_name, task)
        A2AClient->>RemoteAgent: HTTP POST /send_message
        
        Note over RemoteAgent: A2A Protocol Processing
        RemoteAgent->>RemoteExecutor: Process A2A Message
        RemoteExecutor->>RemoteTool: get_availability(start_date, end_date)
        RemoteTool->>Calendar: Query availability
        Calendar-->>RemoteTool: Available time slots
        RemoteTool-->>RemoteExecutor: Formatted availability response
        RemoteExecutor-->>RemoteAgent: A2A Task Result
        RemoteAgent-->>A2AClient: HTTP Response with artifacts
        A2AClient-->>HostAgent: Availability data
    end
    
    Note over HostAgent: Analyze and find common slots
    HostAgent->>HostAgent: Analyze responses + host availability
    HostAgent->>User: Present common available time slots
    
    User->>HostAgent: "Book meeting for 2025-06-13 at 20:00"
    HostAgent->>HostAgent: book_host_meeting(date, start_time, end_time, meeting_name)
    HostAgent->>User: Booking confirmation
```

## 3. Host Agent Schedule Management Flow

```mermaid
flowchart LR
    subgraph "Schedule Management Operations"
        User[User Request] --> Decision{Operation Type?}
        
        Decision -->|View Availability| ViewOp[list_host_availability]
        Decision -->|Book Meeting| BookOp[book_host_meeting]
        Decision -->|Update Schedule| ManageOp[manage_host_availability]
        Decision -->|Query Friends| QueryOp[send_message to agents]
    end
    
    subgraph "Host Schedule Storage"
        HostDB[(HOST_SCHEDULE<br/>In-Memory Dict)]
    end
    
    subgraph "Schedule Operations"
        ViewOp --> ReadOp[Read availability for date]
        BookOp --> WriteOp[Write meeting to time slots]
        ManageOp --> UpdateOp[Update/Add time slots]
    end
    
    ReadOp --> HostDB
    WriteOp --> HostDB  
    UpdateOp --> HostDB
    
    HostDB --> Response[JSON Response]
    Response --> User
    
    subgraph "A2A Network"
        QueryOp --> A2ANet[A2A Protocol Network]
        A2ANet --> FriendResponse[Friend Availability Data]
        FriendResponse --> User
    end
    
    %% Styling
    classDef operation fill:#bbdefb
    classDef storage fill:#c8e6c9
    classDef network fill:#ffe0b2
    
    class ViewOp,BookOp,ManageOp,QueryOp operation
    class HostDB,ReadOp,WriteOp,UpdateOp storage
    class A2ANet,FriendResponse network
```

## 4. Multi-Agent Meeting Scheduling Workflow

```mermaid
graph TD
    Start([User Requests Meeting]) --> HostInit[Host Agent Initialized]
    
    HostInit --> CheckHost{Check Host<br/>Availability}
    CheckHost -->|Available slots found| QueryFriends[Query Friend Agents]
    CheckHost -->|No availability| NoHost[Inform user - Host not available]
    
    QueryFriends --> A2ACall[Send A2A Messages]
    
    subgraph "Parallel A2A Calls"
        A2ACall --> Karley[Karley Coaching<br/>Services Response]
        A2ACall --> Nate[Nate Agent<br/>Response]  
        A2ACall --> Kaitlynn[Kaitlynn Agent<br/>Response]
    end
    
    Karley --> Analyze[Analyze All Responses]
    Nate --> Analyze
    Kaitlynn --> Analyze
    
    Analyze --> CommonSlots{Common Time<br/>Slots Found?}
    
    CommonSlots -->|Yes| Present[Present Options to User]
    CommonSlots -->|No| NoCommon[No common availability found]
    
    Present --> UserChoice{User Selects<br/>Time Slot?}
    UserChoice -->|Yes| BookMeeting[book_host_meeting]
    UserChoice -->|No| Present
    
    BookMeeting --> Confirm[Send Confirmation]
    
    NoHost --> End([End])
    NoCommon --> End
    Confirm --> End
    
    %% Styling
    classDef process fill:#e3f2fd
    classDef decision fill:#fff3e0
    classDef agent fill:#f1f8e9
    classDef endpoint fill:#fce4ec
    
    class HostInit,QueryFriends,A2ACall,Analyze,BookMeeting process
    class CheckHost,CommonSlots,UserChoice decision
    class Karley,Nate,Kaitlynn agent
    class Start,End,NoHost,NoCommon,Present,Confirm endpoint
```