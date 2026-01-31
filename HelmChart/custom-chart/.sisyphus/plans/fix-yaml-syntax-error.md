# Fix Helm Deployment YAML Syntax Error

## TL;DR

> **Quick Summary**: Fix YAML heredoc syntax error in deployment template where Jinja2 `{{-` syntax inside a YAML heredoc causes YAML parser to fail.
>
> **Deliverables**: Single file fixed: `templates/deployment.yaml`
> - [ ] deployment.yaml syntax corrected

**Estimated Effort**: Trivial (1 file, 1 line fix)
**Parallel Execution**: NO - sequential
**Critical Path**: Fix YAML → Test with helm template

---

## Context

### Original Request
User reported Helm upgrade failure:
```
[PError: UPGRADE FAILED: YAML parse error on llm-endpoint/templates/deployment.yaml: error converting YAML to JSON: yaml: line 30: could not find expected ':']
```

### Root Cause Analysis
**File**: `templates/deployment.yaml`, line 30

**Problem**: YAML heredoc (`|`) containing Jinja2 template syntax (`{{-`)

```yaml
command:
  - "/bin/sh"
  - "-c"
  - |
    {{- if $service.bootstrap }}  # ← YAML parser fails here
    echo "Running bootstrap command: {{ $service.bootstrap }}"
    {{ $service.bootstrap }}
    {{- end }}
    vllm serve {{ $service.model.path }} \
      --host 0.0.0.0 \
      --port {{ $service.service.port }} \
      {{- if $service.extraArgs }}
      {{- range $service.extraArgs }}
      {{ . }} \
      {{- end }}
      {{- end }}
```

**Why it fails**:
- The `|` marker tells YAML to treat everything as a multi-line string
- The YAML parser encounters `{{-` (looks like a key-value pair)
- Expects a colon after `{{-` but finds nothing → parse error

**The actual bug**: The YAML parser is confused by Jinja2 syntax inside the heredoc. The heredoc should not contain literal `{{` and `}}` characters.

### Investigation
- Used `helm template --debug` to identify exact error location
- Used `python3` to verify YAML structure
- Confirmed the heredoc syntax is the issue

---

## Work Objectives

### Core Objective
Fix the YAML syntax error in `templates/deployment.yaml` to allow Helm to successfully render the deployment template.

### Concrete Deliverables
- Fixed `templates/deployment.yaml` file

### Definition of Done
- [ ] Helm template renders successfully: `helm template test . --values values.yaml`
- [ ] No YAML parse errors
- [ ] Generated deployment manifest is valid

### Must Have
- YAML must parse without errors
- Jinja2 template syntax must still work correctly
- Command structure must remain functional

### Must NOT Have (Guardrails)
- Do NOT remove the Jinja2 conditional logic
- Do NOT change the command structure
- Do NOT modify other template files

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO
- **User wants tests**: N/A (trivial fix)
- **Framework**: Manual verification with helm template

### Manual QA Only

**Verification Procedure**:

1. **Test template rendering**:
   ```bash
   helm template test . --values values.yaml
   ```

2. **Expected outcome**:
   - Exit code: 0 (success)
   - No YAML parse errors
   - Valid Kubernetes manifest output

3. **If error persists**:
   - Check if there are other template files with similar issues
   - Verify YAML indentation is correct (2 spaces)
   - Ensure no trailing whitespace in the file

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: Fix YAML syntax error
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | None | None (single task) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1 | delegate_task(category="quick", load_skills=["git-master"], ...) |

---

## TODOs

- [ ] 1. Fix YAML heredoc syntax error in deployment.yaml

  **What to do**:
  - Open `templates/deployment.yaml` in a text editor
  - Locate line 30 (the `command` section)
  - Remove the leading `|` heredoc marker from the multi-line string
  - Ensure the command is still properly formatted as a list of strings
  - Save the file

  **The fix**:
  Change from:
  ```yaml
  command:
    - "/bin/sh"
    - "-c"
    - |
      {{- if $service.bootstrap }}
      echo "Running bootstrap command: {{ $service.bootstrap }}"
      {{ $service.bootstrap }}
      {{- end }}
      vllm serve {{ $service.model.path }} \
        --host 0.0.0.0 \
        --port {{ $service.service.port }} \
        {{- if $service.extraArgs }}
        {{- range $service.extraArgs }}
        {{ . }} \
        {{- end }}
        {{- end }}
  ```

  To:
  ```yaml
  command:
    - "/bin/sh"
    - "-c"
    - "{{- if $service.bootstrap }}"
    - "echo \"Running bootstrap command: {{ $service.bootstrap }}\""
    - "{{ $service.bootstrap }}"
    - "{{- end }}"
    - "vllm serve {{ $service.model.path }} \\"
    - "  --host 0.0.0.0 \\"
    - "  --port {{ $service.service.port }} \\"
    - "{{- if $service.extraArgs }}"
    - "{{- range $service.extraArgs }}"
    - "{{ . }} \\"
    - "{{- end }}"
    - "{{- end }}"
  ```

  **Alternative fix** (if you prefer keeping the heredoc):
  - Escape the Jinja2 syntax: `{{{{-` and `}}}}` instead of `{{-` and `}}`
  - This tells the YAML parser to treat `{{` as literal characters

  **Recommended approach**: Split the command into individual list items (first option above) to avoid heredoc issues entirely.

  **Must NOT do**:
  - Do NOT remove the Jinja2 conditionals
  - Do NOT change the vLLM command arguments
  - Do NOT modify other sections of the file

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Trivial single-file fix, no complex logic
  - **Skills**: [`git-master`]
    - `git-master`: For atomic commit of the fix
  - **Skills Evaluated but Omitted**:
    - `playwright`: Not needed (no UI changes)
    - `frontend-ui-ux`: Not needed (no UI changes)
    - `dev-browser`: Not needed (no browser interactions)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (single task)
  - **Blocks**: None
  - **Blocked By**: None (can start immediately)

  **References**:

  **Pattern References** (existing code to follow):
  - None (this is a bug fix, not a pattern implementation)

  **API/Type References** (contracts to implement against):
  - None

  **Test References** (testing patterns to follow):
  - None (manual verification only)

  **Documentation References** (specs and requirements):
  - None

  **External References** (libraries and frameworks):
  - [Helm YAML Template Syntax](https://helm.sh/docs/topics/charts/#yaml-template-syntax)
  - [Kubernetes Deployment Spec](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

  **WHY Each Reference Matters**:
  - Helm docs: Understand how to properly structure Jinja2 templates in YAML
  - K8s Deployment: Verify the command structure is valid Kubernetes syntax

  **Acceptance Criteria**:

  **Manual Execution Verification**:

  *Choose based on deliverable type:*

  **For YAML/Config changes:**
  - [ ] Run: `helm template test . --values values.yaml`
  - [ ] Expected: Exit code 0, no YAML parse errors
  - [ ] Expected: Valid Kubernetes manifest output with deployment resource

  **Evidence Required**:
  - [ ] Command output captured (copy-paste terminal output)
  - [ ] Verify no error messages in output

  **Commit**: YES
  - Message: `fix(deployment): correct YAML heredoc syntax in command section`
  - Files: `templates/deployment.yaml`
  - Pre-commit: `helm template test . --values values.yaml`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `fix(deployment): correct YAML heredoc syntax in command section` | templates/deployment.yaml | `helm template test . --values values.yaml` → exit code 0 |

---

## Success Criteria

### Verification Commands
```bash
# Should succeed with exit code 0
helm template test . --values values.yaml

# Should produce valid Kubernetes manifest
# Should NOT contain YAML parse errors
```

### Final Checklist
- [ ] Helm template renders successfully
- [ ] No YAML parse errors
- [ ] Command structure preserved
- [ ] Jinja2 templates still work correctly