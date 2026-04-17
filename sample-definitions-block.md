```xml
STRUCTURED INPUT TEMPLATE

Structured Input template.
Recommended minimal: contextual_data, instructions_definition, goals_success_definition, payload.

<structured_input>
  <contextual_data>
  [Context, audience, domain, or relevant constraints.]
  </contextual_data>

  <instructions_definition>
  [What should be done to the payload.]
  </instructions_definition>

  <goals_success_definition>
  [Goals and success criteria.]
  </goals_success_definition>

  <payload>
  [Source input.]
  </payload>

  <session_directives>
    <role>
    [Select one Role from the Library.]
    </role>

    <mode>
    [Select one Mode from the Library.]
    </mode>

    <steps>
    [Provide the ordered list of Steps to execute.]
    </steps>

    <loops>
    [Provide the number of loop cycles to run.]
    </loops>

    <step_output>
    [quiet | minimal | full | double]
    </step_output>

    <loop_output>
    [quiet | full]
    </loop_output>

    <final_payload_output>
    [off | full | double]
    </final_payload_output>
  </session_directives>
</structured_input>
```